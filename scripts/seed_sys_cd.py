import asyncio
import os
import sys

# 프로젝트 루트 경로 추가 (apps. 등 임포트 가능하도록)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["USE_REAL_DB"] = "True"

from sqlalchemy import text
from sqlalchemy import text
from apps.api.core.database import AsyncSessionLocal
from apps.api.models.system_code import SystemCodeGroup, SystemCode

import apps.api.models
import apps.services.gpu.models_offering
import apps.services.gpu.models_hardware
import apps.services.gpu.models_provider
import apps.services.gpu.models_history
import apps.services.retail.models
import apps.services.news.models

async def seed_metadata():
    print("Seeding System Code Metadata...")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. SYS_CD_GROUP_BAS 추가
            
            # Clear existing logic
            await session.execute(text("DELETE FROM \"SYS_CD_BAS\""))
            await session.execute(text("DELETE FROM \"SYS_CD_GROUP_BAS\""))
            
            groups = [
                SystemCodeGroup(SYS_GROUP_ID="GPU_PROVIDER", GRP_NM="글로벌 GPU 클라우드 프로바이더", DESC_TXT="크롤링 및 시세 연동 대상 벤더 목록"),
                SystemCodeGroup(SYS_GROUP_ID="FIN_TICKER", GRP_NM="금융 주식 및 선물 티커", DESC_TXT="티커 심볼 매핑용 (SYS_VAL 컬럼 사용)"),
                SystemCodeGroup(SYS_GROUP_ID="HW_TYP", GRP_NM="하드웨어 타입", DESC_TXT="GPU, CPU, DRAM 분류")
            ]
            session.add_all(groups)
            
            # 2. SYS_CD_BAS 추가 - Providers
            providers = [
                ("vast-ai", "Vast.ai (P2P)"),
                ("runpod", "RunPod"),
                ("aws", "Amazon Web Services"),
                ("vessl", "VESSL AI"),
                ("gpuaas", "GPUaaS (한국)"),
                ("cloudv", "CloudV (한국)"),
                ("runyourai", "RunYourAI (한국)"),
                ("gabia", "Gabia (한국)"),
                ("ktcloud", "KT Cloud (한국)"),
                ("xesktop", "Xesktop (한국)"),
                ("ncloud", "Naver Cloud (한국)")
            ]
            
            for provider_id, provider_nm in providers:
                # 숏 약어와 대문자 원칙 적용
                code_id = provider_id.upper().replace("-", "_")
                sys_code = SystemCode(
                    SYS_GROUP_ID="GPU_PROVIDER",
                    SYS_CD_ID=code_id,
                    SYS_CD_NM=provider_nm,
                    REF_VAL_1=provider_id # 원래의 slug를 ref_val_1에 저장
                )
                session.add(sys_code)
                
            # 3. SYS_CD_BAS 추가 - Fin Tickers
            tickers = [
                ("NVDA", "Nvidia Corp", "엔비디아"),
                ("SK_HYNIX", "SK Hynix", "SK하이닉스"),
                ("DRAM_FUTURES", "DRAM Futures", "DRAM 선물 지수")
            ]
            for ticker_id, val, kor_nm in tickers:
                session.add(SystemCode(
                    SYS_GROUP_ID="FIN_TICKER",
                    SYS_CD_ID=ticker_id,
                    SYS_CD_NM=kor_nm,
                    SYS_VAL=val
                ))
                
            # 4. SYS_CD_BAS 추가 - Hardware Types
            hw_types = [
                ("GPU", "GPU 인스턴스/그래픽카드"),
                ("CPU", "CPU 인스턴스/프로세서"),
                ("DRAM", "시스템 메모리")
            ]
            for hw_id, hw_nm in hw_types:
                session.add(SystemCode(
                    SYS_GROUP_ID="HW_TYP",
                    SYS_CD_ID=hw_id,
                    SYS_CD_NM=hw_nm,
                    SYS_VAL=hw_id.lower()
                ))
                
            print("Successfully added all System Code groups and codes.")

if __name__ == "__main__":
    # 데이터베이스 연결 필요 시 환경변수 DATABASE_URL 혹은 USE_REAL_DB=True 필수
    asyncio.run(seed_metadata())
