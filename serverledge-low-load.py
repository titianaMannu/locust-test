import pickle
import random

from locust import HttpUser, TaskSet, task


class ServerledgeLowTask(TaskSet):
    response = None

    @task(1)
    def invoke_low_service_function(self):
        params = {"a": "1", "b": "2"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/sieve", json={
            "Params": pickle.loads(p),
            "QoSClass": 0,
            "QoSMaxRespT": 5,
            "CanDoOffloading": False
        })
        print("response content:", self.response.text)


class UserLowService(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1
    wait_time = lambda self: random.expovariate(3)
