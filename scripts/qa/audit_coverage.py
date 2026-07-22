import os
import ast
import glob
from datetime import datetime
import subprocess

def get_all_python_files(directory):
    return glob.glob(f"{directory}/**/*.py", recursive=True)

def extract_functions_and_classes(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            node = ast.parse(f.read(), filename=filepath)
        except Exception:
            return [], []
            
    functions = [n.name for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
    return functions, classes

def check_test_exists(target_name, test_files):
    # A heuristic: look for "test_{target_name.lower()}" or just the target name inside the test file contents
    target_lower = target_name.lower()
    for test_file in test_files:
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read().lower()
            if target_lower in content:
                return True
    return False

def generate_report():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"qa_audit_{timestamp}.md")
    
    print("Scanning codebase for coverage...")
    target_dirs = ["apps/api", "apps/services"]
    test_files = get_all_python_files("tests")
    
    total_funcs = 0
    covered_funcs = 0
    
    coverage_details = []
    
    for d in target_dirs:
        py_files = get_all_python_files(d)
        for py_file in py_files:
            if "__init__" in py_file:
                continue
            funcs, classes = extract_functions_and_classes(py_file)
            for func in funcs:
                if func.startswith("__"): continue
                total_funcs += 1
                is_covered = check_test_exists(func, test_files)
                if is_covered:
                    covered_funcs += 1
                coverage_details.append(f"- `{'[x]' if is_covered else '[ ]'}` `{py_file}` -> `{func}()`")
                
    coverage_rate = (covered_funcs / total_funcs * 100) if total_funcs > 0 else 0
    
    print("Running pytest...")
    pytest_result = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Codebase QA Audit Report\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## 1. Unit Test Coverage (Heuristic)\n")
        f.write(f"- Total Functions Scanned: {total_funcs}\n")
        f.write(f"- Functions with Tests: {covered_funcs}\n")
        f.write(f"- Estimated Coverage: **{coverage_rate:.2f}%**\n\n")
        
        f.write("### Coverage Details\n")
        f.write("\n".join(coverage_details))
        f.write("\n\n")
        
        f.write("## 2. Pytest Execution Results\n")
        f.write("```text\n")
        f.write(pytest_result.stdout)
        f.write("\n```\n")
        
    print(f"Audit Complete. Report saved to {report_path}")

if __name__ == "__main__":
    generate_report()
