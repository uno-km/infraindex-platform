from locust import HttpUser, task, between

class APIStressUser(HttpUser):
    # This represents a massive influx of users hitting the API
    wait_time = between(0.1, 1.0)
    
    @task(3)
    def test_enterprise_endpoint(self):
        self.client.get("/api/v1/retail/enterprise")
        
    @task(2)
    def test_news_endpoint(self):
        self.client.get("/api/v1/news")
        
    @task(1)
    def test_gpu_endpoint(self):
        self.client.get("/api/v1/gpu/search")
