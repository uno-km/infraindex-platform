import os
import glob
import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# Only replace ORM class name and attribute access (PriceHistory.something)
gpu_replacements = [
    ("import PriceHistory", "import GpuPriceHistory"),
    (" PriceHistory(", " GpuPriceHistory("),
    ("select(PriceHistory)", "select(GpuPriceHistory)"),
    ("PriceHistory.", "GpuPriceHistory."),
    
    ("GpuPriceHistory.provider_id", "GpuPriceHistory.prv_id"),
    ("GpuPriceHistory.hardware_type", "GpuPriceHistory.hw_typ"),
    ("GpuPriceHistory.gpu_model", "GpuPriceHistory.gpu_mdl"),
    ("GpuPriceHistory.price_per_hour", "GpuPriceHistory.prc_ph"),
    ("GpuPriceHistory.availability_status", "GpuPriceHistory.avl_st"),
    ("GpuPriceHistory.timestamp", "GpuPriceHistory.ts"),
    ("GpuPriceHistory.cpu_model", "GpuPriceHistory.cpu_mdl"),
    ("GpuPriceHistory.cores", "GpuPriceHistory.core_cnt"),
    ("GpuPriceHistory.sys_ram_gb", "GpuPriceHistory.sys_ram"),
    ("GpuPriceHistory.provider_link", "GpuPriceHistory.prv_url"),
    
    ("import RetailPriceHistory", "import RtlPriceHistory"),
    (" RetailPriceHistory(", " RtlPriceHistory("),
    ("select(RetailPriceHistory)", "select(RtlPriceHistory)"),
    ("RetailPriceHistory.", "RtlPriceHistory."),
    
    ("RtlPriceHistory.hardware_type", "RtlPriceHistory.hw_typ"),
    ("RtlPriceHistory.model_name", "RtlPriceHistory.mdl_nm"),
    ("RtlPriceHistory.capacity_gb", "RtlPriceHistory.capa_gb"),
    ("RtlPriceHistory.price", "RtlPriceHistory.prc_amt"),
    ("RtlPriceHistory.currency", "RtlPriceHistory.crncy_cd"),
    ("RtlPriceHistory.product_url", "RtlPriceHistory.prd_url"),
    ("RtlPriceHistory.is_official", "RtlPriceHistory.is_offc"),
    ("RtlPriceHistory.platform", "RtlPriceHistory.pltf_nm"),
    ("RtlPriceHistory.timestamp", "RtlPriceHistory.ts"),
    
    ("import FinancialMarketHistory", "import FinMktHistory"),
    (" FinancialMarketHistory(", " FinMktHistory("),
    ("select(FinancialMarketHistory)", "select(FinMktHistory)"),
    ("FinancialMarketHistory.", "FinMktHistory."),
    
    ("FinMktHistory.asset_type", "FinMktHistory.ast_typ"),
    ("FinMktHistory.symbol", "FinMktHistory.sym_cd"),
    ("FinMktHistory.open", "FinMktHistory.opn_prc"),
    ("FinMktHistory.high", "FinMktHistory.hi_prc"),
    ("FinMktHistory.low", "FinMktHistory.lo_prc"),
    ("FinMktHistory.close", "FinMktHistory.cls_prc"),
    ("FinMktHistory.volume", "FinMktHistory.vol_cnt"),
    ("FinMktHistory.currency", "FinMktHistory.crncy_cd"),
    ("FinMktHistory.timestamp", "FinMktHistory.ts"),
    
    ("import NewsArticle", "import NewsArticle"), # name didn't change
    ("NewsArticle.title", "NewsArticle.titl_nm"),
    ("NewsArticle.url", "NewsArticle.arti_url"),
    ("NewsArticle.source", "NewsArticle.src_nm"),
    ("NewsArticle.published_at", "NewsArticle.pub_ts"),
    ("NewsArticle.summary", "NewsArticle.sum_txt"),
    ("NewsArticle.keywords", "NewsArticle.kwd_txt"),
    ("NewsArticle.collection_tier", "NewsArticle.clct_tr"),
    ("NewsArticle.timestamp", "NewsArticle.crt_ts"),
]

search_paths = [
    "apps/**/*.py"
]

files_to_check = []
for p in search_paths:
    files_to_check.extend(glob.glob(p, recursive=True))

for fpath in files_to_check:
    if os.path.basename(fpath) in ["models_history.py", "models.py", "outbox.py", "system_code.py", "data_service.py"]:
        continue
        
    replace_in_file(fpath, gpu_replacements)
