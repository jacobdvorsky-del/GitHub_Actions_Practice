import requests

class TasksAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_tasks(self):
        return requests.get(f"{self.base_url}/api/tasks")

    def get_task(self, id: int):
        return requests.get(f"{self.base_url}/api/tasks/{id}")

    def create_task(self, payload: dict):
        return requests.post(f"{self.base_url}/api/tasks", json=payload)

    def update_task(self, id: int, payload: dict):
        return requests.put(f"{self.base_url}/api/tasks/{id}", json=payload)

    def delete_task(self, id: int):
        return requests.delete(f"{self.base_url}/api/tasks/{id}")