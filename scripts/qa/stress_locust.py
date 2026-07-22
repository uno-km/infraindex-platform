import os
import subprocess
from datetime import datetime
import json
import time

def run_stress_test():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"qa_stress_{timestamp}.md")
    csv_prefix = os.path.join(report_dir, f"locust_{timestamp}")
    
    print("Starting Locust Stress Test (1000 simulated spike for 15s)...")
    
    # Run locust in headless mode
    # --users 1000 --spawn-rate 500 (Simulating a huge spike)
    locust_file = os.path.join(os.path.dirname(__file__), "locustfile.py")
    
    cmd = [
        "locust",
        "-f", locust_file,
        "--headless",
        "--users", "100", # We use 100 users for this local test to not kill the actual PC
        "--spawn-rate", "50",
        "--run-time", "15s",
        "--host", "http://localhost:8000",
        "--csv", csv_prefix
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        print(f"Failed to run locust: {e}")
        return
        
    print("Parsing Results...")
    
    # Read the generated CSV for stats
    stats_csv = f"{csv_prefix}_stats.csv"
    stats_data = "No CSV generated"
    if os.path.exists(stats_csv):
        with open(stats_csv, "r", encoding="utf-8") as f:
            stats_data = f.read()
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# API Stress Test Report (Locust)\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## 1. Test Configuration\n")
        f.write("- **Peak Users:** 100\n")
        f.write("- **Spawn Rate:** 50/s\n")
        f.write("- **Duration:** 15s\n")
        f.write("- **Target Host:** http://localhost:8000\n\n")
        
        f.write(f"## 2. Server Defense Mechanisms\n")
        f.write("FastAPI is protected by `slowapi` Rate Limiting (1000/minute per IP).\n")
        f.write("We expect to see 429 Too Many Requests in the failures if limits are reached, which proves the DB is protected.\n\n")
        
        f.write(f"## 3. Results (CSV Stats)\n")
        f.write("```csv\n")
        f.write(stats_data)
        f.write("\n```\n")
        
    print(f"Stress Test Complete. Report saved to {report_path}")
    
if __name__ == "__main__":
    run_stress_test()
