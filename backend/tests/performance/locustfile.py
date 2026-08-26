from locust import HttpUser, task, between

class RoadCareUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def get_health(self):
        self.client.get("/health")
        
    @task(3)
    def get_reports(self):
        # Public reports access
        self.client.get("/api/v1/reports?limit=10")
        
    @task(2)
    def get_zones(self):
        self.client.get("/api/v1/zones")

    @task(1)
    def root(self):
        self.client.get("/")
