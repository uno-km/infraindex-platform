from fastapi.testclient import TestClient
from apps.api.main import app
client = TestClient(app)
try:
    response = client.get('/api/v1/chart/candlestick?gpu_model_id=aws')
    print(response.status_code)
    print(response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
