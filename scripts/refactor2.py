import os
import shutil
from pathlib import Path

MOVES = {
    # GPU Models
    "apps/api/models/hardware.py": "apps/services/gpu/models_hardware.py",
    "apps/api/models/offering.py": "apps/services/gpu/models_offering.py",
    "apps/api/models/history.py": "apps/services/gpu/models_history.py",
    "apps/api/models/provider.py": "apps/services/gpu/models_provider.py",
    
    # GPU Crawlers
    "apps/worker/providers/aws.py": "apps/services/gpu/crawler_aws.py",
    "apps/worker/providers/korean.py": "apps/services/gpu/crawler_korean.py",
    "apps/worker/providers/foreign.py": "apps/services/gpu/crawler_foreign.py",
    "apps/worker/providers/runpod.py": "apps/services/gpu/crawler_runpod.py",
    "apps/worker/providers/vast.py": "apps/services/gpu/crawler_vast.py",
}

REPLACEMENTS = {
    # Models
    "apps.api.models.hardware": "apps.services.gpu.models_hardware",
    "apps.api.models.offering": "apps.services.gpu.models_offering",
    "apps.api.models.history": "apps.services.gpu.models_history",
    "apps.api.models.provider": "apps.services.gpu.models_provider",
    
    # Crawlers
    "apps.worker.providers.aws": "apps.services.gpu.crawler_aws",
    "apps.worker.providers.korean": "apps.services.gpu.crawler_korean",
    "apps.worker.providers.foreign": "apps.services.gpu.crawler_foreign",
    "apps.worker.providers.runpod": "apps.services.gpu.crawler_runpod",
    "apps.worker.providers.vast": "apps.services.gpu.crawler_vast",
}

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
    targets = list(root.glob("apps/**/*.py")) + list(root.glob("tests/**/*.py")) + list(root.glob("*.py"))
    
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
    print("Moving files...")
    move_files()
    print("Updating imports...")
    update_imports()
    print("Refactoring part 2 complete.")
