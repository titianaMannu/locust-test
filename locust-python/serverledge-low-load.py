import random

from locust import HttpUser, TaskSet, task


class ServerledgeLowTask(TaskSet):
    response = None

    @task(1)
    def invoke_low_service_function(self):
        self.response = self.client.post("/invoke/sieve", json={
            "QoSClass": 0,
            "QoSMaxRespT": 5,
            "CanDoOffloading": True
        })
        print("response content:", self.response.text)


class UserLowService(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1
    wait_time = lambda self: random.expovariate(3)
