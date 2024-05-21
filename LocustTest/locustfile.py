import time
from locust import HttpUser, task, between

count = 0
class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        print("Hello World")


    def on_start(self):
        response = self.client.post("/api/login",
                                    json={"username": "qadriver",
                                          "password": "Hsmfwfyfef7!"},
                                    headers={'Accept-Language': 'en', 'Content-Type': 'application/json'})
        print(response.json())