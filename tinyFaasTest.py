
import random

from locust import HttpUser, TaskSet, task


class ServerledgeLowTask(TaskSet):
    response = None

    @task(1)
    def invoke_tiny_function(self):
        self.response = self.client.get("http://192.168.1.89:80/sieve")
        print("response content:", self.response.text)


class UserLowService(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1
    wait_time = lambda self: random.expovariate(3)