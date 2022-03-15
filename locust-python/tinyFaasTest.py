import random

from locust import HttpUser, TaskSet, task


class TinyTask(TaskSet):
    response = None

    @task(1)
    def invoke_tiny_function(self):
        self.response = self.client.get("/sieve")
        print("response content:", self.response.text)


class UserTinyService(HttpUser):
    tasks = [TinyTask]
    weight = 1
    wait_time = lambda self: random.expovariate(2)
