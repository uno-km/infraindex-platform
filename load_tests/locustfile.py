from locust import HttpUser, task, between
import random

class InfraIndexUser(HttpUser):
    # Simulate users thinking between 1 and 3 seconds between actions
    wait_time = between(1.0, 3.0)

    @task(3)
    def search_gpus(self):
        """Simulate users searching for high-demand GPUs like H100"""
        queries = ["H100", "A100", "RTX 4090", "에이치백", "4090"]
        query = random.choice(queries)
        self.client.get(f"/api/v1/search/gpus?q={query}")

    @task(2)
    def view_price_chart(self):
        """Simulate users viewing the time-series price chart"""
        models = ["H100", "A100"]
        model_id = random.choice(models)
        self.client.get(f"/api/v1/chart/price-series?gpu_model_id={model_id}")

    @task(1)
    def download_reports(self):
        """Simulate users hitting the heavy export APIs"""
        self.client.get("/api/v1/reports/daily-brief")
        # In a real heavy load test, we might also hit the Excel/Word export, 
        # but for stability testing, we'll focus on the JSON brief endpoint to prevent memory exhaustion on local.
        # self.client.get("/api/v1/reports/excel")
