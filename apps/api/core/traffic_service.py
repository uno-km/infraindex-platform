import os
import json
from apps.api.core.config import settings

class TrafficService:
    def __init__(self):
        self.file_path = os.path.join(settings.LOCAL_STORAGE_DIR, "traffic.json")
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(settings.LOCAL_STORAGE_DIR):
            os.makedirs(settings.LOCAL_STORAGE_DIR)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def increment_view(self, resource_id: str):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}

        data[resource_id] = data.get(resource_id, 0) + 1

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return data[resource_id]

    def get_all_traffic(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

traffic_service = TrafficService()
