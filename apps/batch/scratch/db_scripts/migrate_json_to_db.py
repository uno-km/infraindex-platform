import os
import glob
import json
import asyncio
import sys
from datetime import datetime

# Setup path and env for standalone script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["USE_REAL_DB"] = "True"

import shared.models
from shared.db.session import AsyncSessionLocal
from sqlalchemy import text
from apps.batch.services.gpu.models_history import GpuPriceHistory
import apps.batch.services.gpu.models_offering
import apps.batch.services.gpu.models_hardware
import apps.batch.services.gpu.models_provider
import apps.batch.services.retail.models
import shared.models.news
import apps.batch.services.financial.models

from shared.models.news import NewsArticle
from shared.models.retail import RtlPriceHistory
from apps.batch.services.financial.models import FinMktHistory

async def migrate_json_to_db():
    print("Starting JSON to DB migration...")
    
    # 1. Read all JSON files
    json_files = glob.glob(os.path.join("data", "*.json"))
    json_files.extend(glob.glob(os.path.join("data", "crawled", "*.json")))
    
    all_data = []
    for filepath in json_files:
        if "traffic.json" in filepath: 
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item["_source_filepath"] = filepath
                    all_data.extend(data)
                elif isinstance(data, dict):
                    # Handle if there's a wrapper key like "data"
                    if "data" in data and isinstance(data["data"], list):
                        for item in data["data"]:
                            item["_source_filepath"] = filepath
                        all_data.extend(data["data"])
                    elif "offerings" in data and isinstance(data["offerings"], list):
                        for item in data["offerings"]:
                            item["_source_filepath"] = filepath
                        all_data.extend(data["offerings"])
                    else:
                        data["_source_filepath"] = filepath
                        all_data.append(data)
        except Exception as e:
            print(f"Could not read {filepath}: {e}")

    print(f"Loaded {len(all_data)} records from JSON.")

    if not all_data:
        print("No data found to migrate.")
        return

    # 2. Insert into DB
    added_count = 0
    async with AsyncSessionLocal() as session:
        # Clear existing data first to prevent duplicates
        await session.execute(text("TRUNCATE TABLE tbl_gpu_prc_hist RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE tbl_news_arti RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE tbl_rtl_prc_hist RESTART IDENTITY CASCADE"))
        await session.execute(text("TRUNCATE TABLE tbl_fin_mkt_hist RESTART IDENTITY CASCADE"))
        await session.commit()
        print("Cleared existing records in all target tables.")
        
        seen_news_urls = set()
        async with session.begin():
            for item in all_data:
                src_fp = item.get("_source_filepath", "")
                filename = os.path.basename(src_fp)
                
                # Common Timestamp Extraction
                ts_str = item.get("timestamp")
                item_ts = None
                if ts_str:
                    try:
                        from dateutil import parser
                        item_ts = parser.parse(ts_str)
                    except: pass
                
                if not item_ts:
                    import re
                    match = re.search(r'_(\d{8}_\d{6})\.json', filename)
                    if match:
                        try:
                            item_ts = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
                        except:
                            item_ts = datetime.now()
                    else:
                        item_ts = datetime.now()
                
                if item_ts.tzinfo is None:
                    from datetime import timezone
                    item_ts = item_ts.replace(tzinfo=timezone.utc)

                # Branching Logic Based on Filename
                if filename.startswith("news_"):
                    # Process NewsArticle
                    a_url = item.get("url") or item.get("arti_url") or item.get("link") or "Unknown_URL"
                    if a_url in seen_news_urls:
                        continue
                    seen_news_urls.add(a_url)
                    
                    record = NewsArticle(
                        titl_nm=item.get("title") or item.get("titl_nm") or "Untitled",
                        arti_url=a_url,
                        src_nm=item.get("source") or item.get("src_nm") or "Unknown",
                        pub_ts=item_ts, # Use extracted timestamp as published date
                        sum_txt=item.get("summary") or item.get("content"),
                        kwd_txt=",".join(item.get("keywords", []) if isinstance(item.get("keywords"), list) else [str(item.get("keywords", ""))]),
                        clct_tr="migration",
                        crt_ts=datetime.now(timezone.utc)
                    )
                    session.add(record)
                    added_count += 1
                    continue
                    
                elif filename.startswith("stock_prices_"):
                    # Process FinMktHistory
                    record = FinMktHistory(
                        ast_typ="stock",
                        sym_cd=item.get("ticker") or item.get("symbol") or "UNKNOWN",
                        opn_prc=float(item.get("open") or 0.0),
                        hi_prc=float(item.get("high") or 0.0),
                        lo_prc=float(item.get("low") or 0.0),
                        cls_prc=float(item.get("close") or item.get("price") or 0.0),
                        vol_cnt=float(item.get("volume") or 0.0),
                        crncy_cd="USD",
                        ts=item_ts
                    )
                    session.add(record)
                    added_count += 1
                    continue

                elif filename.startswith("gpu_prices_"):
                    # Process RtlPriceHistory (Enterprise/Retail)
                    record = RtlPriceHistory(
                        pltf_nm=item.get("provider") or item.get("vendor") or "unknown",
                        hw_typ=item.get("hw_typ") or item.get("type") or "gpu",
                        mfg_nm=item.get("manufacturer") or item.get("mfg_nm"),
                        mdl_nm=item.get("gpu_model") or item.get("gpuName") or item.get("model") or "unknown",
                        capa_gb=float(item.get("vram_gb") or item.get("memoryInGb") or 0),
                        prc_amt=float(item.get("price_per_hour") or item.get("price") or 0.0),
                        crncy_cd="KRW", # Assuming crawled retail prices are mostly KRW
                        prd_url=item.get("provider_link") or item.get("url"),
                        is_offc=False,
                        ts=item_ts
                    )
                    session.add(record)
                    added_count += 1
                    continue

                # Default: Process GpuPriceHistory (Cloud instances)
                prv = item.get("provider") or item.get("vendor") or "unknown"
                gpu = item.get("gpu_model") or item.get("gpuName") or item.get("model") or "unknown"
                prc = item.get("price_per_hour") or item.get("price")
                
                if prc is None:
                    continue # Skip invalid
                
                try:
                    prc_val = float(prc)
                    if prc_val > 10000:
                        prc_val = prc_val / 1400.0 # KRW to USD heuristic
                except (ValueError, TypeError):
                    continue
                    
                vram = item.get("vram_gb") or item.get("memoryInGb") or item.get("vram")
                try:
                    vram_val = float(vram) if vram is not None else None
                except:
                    vram_val = None

                record = GpuPriceHistory(
                    hw_typ="gpu",
                    prv_id=str(prv).lower(),
                    gpu_mdl=str(gpu).upper(),
                    cpu_mdl=item.get("cpu_model") or item.get("cpu"),
                    vram_gb=vram_val,
                    core_cnt=item.get("cores") or item.get("cpuCores"),
                    prc_ph=prc_val,
                    avl_st=str(item.get("availability_status", "AVAILABLE")),
                    prv_url=item.get("provider_link") or item.get("url"),
                    sys_ram=item.get("sys_ram_gb") or item.get("sysRam"),
                    tdp_w=item.get("tdp_w"),
                    ts=item_ts
                )
                session.add(record)
                added_count += 1
                
    print(f"Successfully migrated {added_count} records into the PostgreSQL database!")

if __name__ == "__main__":
    asyncio.run(migrate_json_to_db())
