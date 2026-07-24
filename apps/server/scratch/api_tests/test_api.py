import urllib.request
print(urllib.request.urlopen('http://localhost:8000/api/v1/chart/candlestick?gpu_model_id=aws').read().decode())
