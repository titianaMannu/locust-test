import pickle
import random

from locust import HttpUser, TaskSet, task


class ServerledgeHighPerfTask(TaskSet):
    response = None

    @task(1)
    def invoke_low_service_function(self):
        params = {"a": "1", "b": "2"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/sieve", json={
            "Params": pickle.loads(p),
            "QoSClass": 1,
            "QoSMaxRespT": 3,
            "CanDoOffloading": False
        })
        print("response content:", self.response.text)


class UserHighPerfService(HttpUser):
    tasks = [ServerledgeHighPerfTask]
    weight = 1
    wait_time = lambda self: random.expovariate(1)
