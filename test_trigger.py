import asyncio
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app, base_url="http://localhost")

print("Sending POST request to trigger financial batch (target: financial)...")
response = client.post("/api/v1/admin/batch/trigger", json={"target": "financial"}, headers={"Host": "localhost"})

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
