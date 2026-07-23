import asyncio
import os
import sys

# 프로젝트 루트 경로 추가 (apps. 등 임포트 가능하도록)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["USE_REAL_DB"] = "True"

from apps.api.core.database import AsyncSessionLocal
from apps.api.models.system_code import SystemCodeGroup, SystemCode

async def seed_metadata():
    print("Seeding System Code Metadata...")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. SYS_CD_GROUP_BAS 추가
            gpu_group = SystemCodeGroup(
                SYS_GROUP_ID="GPU_PROVIDER",
                GRP_NM="글로벌 GPU 클라우드 프로바이더",
                DESC_TXT="크롤링 및 시세 연동 대상 벤더 목록"
            )
            session.add(gpu_group)
            
            # 2. SYS_CD_BAS 추가
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
                
            print("Successfully added GPU_PROVIDER group and codes.")

if __name__ == "__main__":
    # 데이터베이스 연결 필요 시 환경변수 DATABASE_URL 혹은 USE_REAL_DB=True 필수
    asyncio.run(seed_metadata())
