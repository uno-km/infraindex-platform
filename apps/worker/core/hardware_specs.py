from typing import Dict, Any

GPU_SPECS_DB = {
    "RTX 4090": {"tdp_w": 450, "sys_ram_gb": 64},
    "RTX 3090": {"tdp_w": 350, "sys_ram_gb": 48},
    "A100": {"tdp_w": 400, "sys_ram_gb": 128},
    "H100": {"tdp_w": 700, "sys_ram_gb": 256},
    "RTX 4080": {"tdp_w": 320, "sys_ram_gb": 32},
    "RTX 3080": {"tdp_w": 320, "sys_ram_gb": 32},
    "A6000": {"tdp_w": 300, "sys_ram_gb": 128},
    "V100": {"tdp_w": 300, "sys_ram_gb": 64},
    "L40S": {"tdp_w": 350, "sys_ram_gb": 128},
}

def enrich_hardware_specs(gpu_name: str) -> Dict[str, Any]:
    name_upper = gpu_name.upper()
    best_match = {"tdp_w": 250, "sys_ram_gb": 32} # Default fallback
    
    for model, specs in GPU_SPECS_DB.items():
        if model.upper() in name_upper:
            best_match = specs
            break
            
    return best_match
