import glob, os, re, json
from datetime import datetime
from dateutil import parser
json_files = glob.glob(os.path.join("data", "*.json"))
json_files.extend(glob.glob(os.path.join("data", "crawled", "*.json")))

for filepath in json_files:
    if "traffic" in filepath: continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # just check the first item
            item = data[0] if isinstance(data, list) else data
            if "data" in data and isinstance(data["data"], list) and data["data"]: item = data["data"][0]
            if "offerings" in data and isinstance(data["offerings"], list) and data["offerings"]: item = data["offerings"][0]

            ts_str = item.get("timestamp")
            item_ts = None
            if ts_str:
                try: item_ts = parser.parse(ts_str)
                except: pass
            
            if not item_ts:
                match = re.search(r'_(\d{8}_\d{6})\.json', filepath)
                if match:
                    item_ts = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
                else:
                    item_ts = datetime.now()
            print(f"{filepath} -> {item_ts}")
    except Exception as e:
        print(f"Error {filepath}: {e}")
