import requests

class HealthAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_health(self):
        return requests.get(f"{self.base_url}/health")
