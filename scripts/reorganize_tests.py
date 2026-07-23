import os
import shutil

base_backend = "tests/unit"
base_frontend = "apps/web/tests"

backend_moves = {
    "api/API-92b9d69c_admin_test.py": "domains/auth/API-92b9d69c_admin_test.py",
    "api/API-92b9d69c_auth_test.py": "domains/auth/API-92b9d69c_auth_test.py",
    "core/COR-92b9d69c_security_test.py": "domains/auth/COR-92b9d69c_security_test.py",

    "api/API-92b9d69c_users_test.py": "domains/users/API-92b9d69c_users_test.py",

    "api/API-92b9d69c_memory_test.py": "domains/crawler/API-92b9d69c_memory_test.py",
    "api/API-92b9d69c_storage_test.py": "domains/crawler/API-92b9d69c_storage_test.py",
    "schemas/SCH-92b9d69c_gpu_schema_test.py": "domains/crawler/SCH-92b9d69c_gpu_schema_test.py",
    "schemas/SCH-92b9d69c_memory_schema_test.py": "domains/crawler/SCH-92b9d69c_memory_schema_test.py",
    "schemas/SCH-92b9d69c_offer_schema_test.py": "domains/crawler/SCH-92b9d69c_offer_schema_test.py",
    "schemas/SCH-92b9d69c_provider_schema_test.py": "domains/crawler/SCH-92b9d69c_provider_schema_test.py",
    "schemas/SCH-92b9d69c_storage_schema_test.py": "domains/crawler/SCH-92b9d69c_storage_schema_test.py",
    "schemas/SCH-92b9d69c_search_schema_test.py": "domains/crawler/SCH-92b9d69c_search_schema_test.py",
    "worker/WRK-92b9d69c_batch_runner_test.py": "domains/crawler/WRK-92b9d69c_batch_runner_test.py",
    "worker/WRK-92b9d69c_orchestrator_test.py": "domains/crawler/WRK-92b9d69c_orchestrator_test.py",
    "worker/WRK-92b9d69c_outbox_publisher_test.py": "domains/crawler/WRK-92b9d69c_outbox_publisher_test.py",
    "worker/WRK-92b9d69c_tasks_root_test.py": "domains/crawler/WRK-92b9d69c_tasks_root_test.py",
    "core/COR-92b9d69c_data_service_test.py": "domains/crawler/COR-92b9d69c_data_service_test.py",
    "api/API-92b9d69c_search_test.py": "domains/crawler/API-92b9d69c_search_test.py",

    "core/COR-92b9d69c_config_test.py": "domains/infrastructure/COR-92b9d69c_config_test.py",
    "core/COR-92b9d69c_database_test.py": "domains/infrastructure/COR-92b9d69c_database_test.py",
    "core/COR-92b9d69c_redis_client_test.py": "domains/infrastructure/COR-92b9d69c_redis_client_test.py",
    "core/COR-92b9d69c_limiter_test.py": "domains/infrastructure/COR-92b9d69c_limiter_test.py",
    "core/COR-92b9d69c_middleware_test.py": "domains/infrastructure/COR-92b9d69c_middleware_test.py",
    "api/API-92b9d69c_health_test.py": "domains/infrastructure/API-92b9d69c_health_test.py",

    "api/API-92b9d69c_chat_test.py": "domains/ai_chat/API-92b9d69c_chat_test.py",
    "core/COR-92b9d69c_ai_service_test.py": "domains/ai_chat/COR-92b9d69c_ai_service_test.py",

    "api/API-92b9d69c_chart_test.py": "domains/analytics/API-92b9d69c_chart_test.py",
    "api/API-92b9d69c_reports_test.py": "domains/analytics/API-92b9d69c_reports_test.py",
    "api/API-92b9d69c_traffic_test.py": "domains/analytics/API-92b9d69c_traffic_test.py",
    "core/COR-92b9d69c_traffic_service_test.py": "domains/analytics/COR-92b9d69c_traffic_service_test.py",
    "api/API-92b9d69c_stream_test.py": "domains/analytics/API-92b9d69c_stream_test.py",

    "api/API-92b9d69c_history_test.py": "domains/history/API-92b9d69c_history_test.py"
}

frontend_moves = {
    "context/CTX-92b9d69c_AuthContext.test.tsx": "domains/auth/CTX-92b9d69c_AuthContext.test.tsx",
    "components/UI-92b9d69c_LoginModal.test.tsx": "domains/auth/UI-92b9d69c_LoginModal.test.tsx",
    "app/PAG-92b9d69c_AdminPage.test.tsx": "domains/auth/PAG-92b9d69c_AdminPage.test.tsx",

    "components/UI-92b9d69c_GpuDashboard.test.tsx": "domains/crawler/UI-92b9d69c_GpuDashboard.test.tsx",
    "components/UI-92b9d69c_NewsDashboard.test.tsx": "domains/crawler/UI-92b9d69c_NewsDashboard.test.tsx",
    "components/UI-92b9d69c_RetailDashboard.test.tsx": "domains/crawler/UI-92b9d69c_RetailDashboard.test.tsx",
    "components/UI-92b9d69c_EnterpriseDashboard.test.tsx": "domains/crawler/UI-92b9d69c_EnterpriseDashboard.test.tsx",
    "app/PAG-92b9d69c_MemoryPage.test.tsx": "domains/crawler/PAG-92b9d69c_MemoryPage.test.tsx",
    "app/PAG-92b9d69c_StoragePage.test.tsx": "domains/crawler/PAG-92b9d69c_StoragePage.test.tsx",

    "app/PAG-92b9d69c_ChartPage.test.tsx": "domains/analytics/PAG-92b9d69c_ChartPage.test.tsx",
    "app/PAG-92b9d69c_ReportsPage.test.tsx": "domains/analytics/PAG-92b9d69c_ReportsPage.test.tsx",
    "components/UI-92b9d69c_InsightDashboard.test.tsx": "domains/analytics/UI-92b9d69c_InsightDashboard.test.tsx",

    "components/UI-92b9d69c_Header.test.tsx": "domains/core/UI-92b9d69c_Header.test.tsx",
    "components/UI-92b9d69c_TabButton.test.tsx": "domains/core/UI-92b9d69c_TabButton.test.tsx",
    "app/PAG-92b9d69c_RootPage.test.tsx": "domains/core/PAG-92b9d69c_RootPage.test.tsx"
}

def move_files(moves_dict, base_dir):
    for src_rel, dst_rel in moves_dict.items():
        src = os.path.join(base_dir, src_rel)
        dst = os.path.join(base_dir, dst_rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
        else:
            print(f"File not found, skipping: {src}")

if __name__ == "__main__":
    print("Moving backend tests...")
    move_files(backend_moves, base_backend)
    
    print("Moving frontend tests...")
    move_files(frontend_moves, base_frontend)
    
    print("Test reorganization complete.")
