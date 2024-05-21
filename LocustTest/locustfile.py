import time
from locust import HttpUser, task, between

count = 0
class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        print("Hello World")


    def on_start(self):
        print("ON START: ")