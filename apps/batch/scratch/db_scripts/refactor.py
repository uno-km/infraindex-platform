import os
import shutil
from pathlib import Path

# Mapping of file source to file destination
MOVES = {
    # GPU
    "apps/api/models/gpu.py": "apps/services/gpu/models.py",
    "apps/api/api/v1/endpoints/gpus.py": "apps/services/gpu/router_gpus.py",
    "apps/api/api/v1/endpoints/providers.py": "apps/services/gpu/router_providers.py",
    "apps/worker/providers/gpu.py": "apps/services/gpu/crawler.py",
    
    # CPU
    "apps/worker/providers/cpu.py": "apps/services/cpu/crawler.py",
    
    # Retail
    "apps/api/models/retail.py": "apps/services/retail/models.py",
    "apps/api/api/v1/endpoints/retail_charts.py": "apps/services/retail/router.py",
    "apps/worker/providers/retail.py": "apps/services/retail/crawler.py",
    "apps/worker/tasks/retail.py": "apps/services/retail/tasks.py",
    
    # Financial
    "apps/api/models/financial.py": "apps/services/financial/models.py",
    "apps/api/api/v1/endpoints/insights.py": "apps/services/financial/router.py",
    "apps/worker/providers/financial.py": "apps/services/financial/crawler.py",
    "apps/worker/tasks/financial.py": "apps/services/financial/tasks.py",
    
    # News
    "apps/api/models/news.py": "apps/services/news/models.py",
    "apps/api/api/v1/endpoints/news.py": "apps/services/news/router.py",
    "apps/worker/providers/news.py": "apps/services/news/crawler.py",
    "apps/worker/tasks/news.py": "apps/services/news/tasks.py",
}

# Import string replacements
REPLACEMENTS = {
    # Models
    "apps.server.models.gpu": "apps.batch.services.gpu.models",
    "apps.server.models.retail": "apps.batch.services.retail.models",
    "apps.server.models.financial": "apps.batch.services.financial.models",
    "apps.server.models.news": "apps.batch.services.news.models",
    
    # Endpoints
    "apps.server.api.v1.endpoints.gpus": "apps.batch.services.gpu.router_gpus",
    "apps.server.api.v1.endpoints.providers": "apps.batch.services.gpu.router_providers",
    "apps.server.api.v1.endpoints.retail_charts": "apps.batch.services.retail.router",
    "apps.server.api.v1.endpoints.insights": "apps.batch.services.financial.router",
    "apps.server.api.v1.endpoints.news": "apps.batch.services.news.router",
    
    # Crawlers
    "apps.batch.worker.providers.gpu": "apps.batch.services.gpu.crawler",
    "apps.batch.worker.providers.cpu": "apps.batch.services.cpu.crawler",
    "apps.batch.worker.providers.retail": "apps.batch.services.retail.crawler",
    "apps.batch.worker.providers.financial": "apps.batch.services.financial.crawler",
    "apps.batch.worker.providers.news": "apps.batch.services.news.crawler",
    
    # Tasks
    "apps.batch.worker.tasks.retail": "apps.batch.services.retail.tasks",
    "apps.batch.worker.tasks.financial": "apps.batch.services.financial.tasks",
    "apps.batch.worker.tasks.news": "apps.batch.services.news.tasks",
}

def create_dirs():
    domains = set(Path(dest).parent for dest in MOVES.values())
    for d in domains:
        d.mkdir(parents=True, exist_ok=True)
        # Create __init__.py so Python recognizes them as modules
        (d / "__init__.py").touch(exist_ok=True)

def move_files():
    for src, dest in MOVES.items():
        src_path = Path(src)
        dest_path = Path(dest)
        if src_path.exists():
            print(f"Moving {src} -> {dest}")
            shutil.move(str(src_path), str(dest_path))
        else:
            print(f"Skipping {src} (not found)")

def update_imports():
    root = Path(".")
    targets = list(root.glob("apps/**/*.py")) + list(root.glob("tests/**/*.py"))
    
    for py_file in targets:
        try:
            content = py_file.read_text(encoding="utf-8")
            original = content
            for old, new in REPLACEMENTS.items():
                content = content.replace(old, new)
            
            if content != original:
                py_file.write_text(content, encoding="utf-8")
                print(f"Updated imports in {py_file}")
        except Exception as e:
            print(f"Error reading {py_file}: {e}")

if __name__ == "__main__":
    print("Creating domain directories...")
    create_dirs()
    print("Moving files...")
    move_files()
    print("Updating imports...")
    update_imports()
    print("Refactoring complete.")
