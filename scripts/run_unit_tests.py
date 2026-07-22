import json
import subprocess
import sys
import argparse
from pathlib import Path

REGISTRY_FILE = "test_registry.json"

def load_registry():
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {REGISTRY_FILE} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: {REGISTRY_FILE} is not a valid JSON.")
        sys.exit(1)

def verify_registry(registry):
    print("Verifying test registry integrity...\n")
    missing = False
    
    for svc_id, metadata in registry.items():
        print(f"[{svc_id}] - {metadata['domain']}")
        
        for tf in metadata.get("target_files", []):
            if not Path(tf).exists():
                print(f"  [X] Missing target file: {tf}")
                missing = True
        
        for test in metadata.get("test_files", []):
            if not Path(test).exists():
                print(f"  [X] Missing test file: {test}")
                missing = True
                
    if missing:
        print("\nVerification FAILED. Some files are missing.")
        sys.exit(1)
    else:
        print("\n[OK] Verification PASSED. All mapped files exist.")

def run_tests(service_id=None):
    registry = load_registry()
    
    if service_id:
        if service_id not in registry:
            print(f"Error: Service ID '{service_id}' not found in registry.")
            sys.exit(1)
            
        test_files = registry[service_id].get("test_files", [])
        if not test_files:
            print(f"Warning: No test files registered for {service_id}")
            sys.exit(0)
            
        print(f"\n🚀 Running tests for {service_id} ({registry[service_id]['domain']})...")
        cmd = ["pytest", "-v"] + test_files
    else:
        print("\n🚀 Running all registered unit tests...")
        test_files = []
        for meta in registry.values():
            test_files.extend(meta.get("test_files", []))
            
        if not test_files:
            print("No test files found in registry.")
            sys.exit(0)
            
        cmd = ["pytest", "-v"] + list(set(test_files))
        
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ All specified tests passed!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test execution failed with exit code {e.returncode}.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test runner via Service Registry")
    parser.add_argument("--verify", action="store_true", help="Verify that all mapped files exist")
    parser.add_argument("--service", type=str, help="Run tests for a specific Service ID (e.g. GPU-001)")
    
    args = parser.parse_args()
    
    if args.verify:
        registry = load_registry()
        verify_registry(registry)
    else:
        run_tests(args.service)
