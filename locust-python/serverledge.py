import pickle
import random

from locust import HttpUser, TaskSet, task


class ServerledgeHighPerfTask(TaskSet):
    response = None

    @task(2)
    def invoke_hp1_service_function(self):
        self.response = self.client.post("/invoke/sieve", json={
            "QoSClass": 1,
            "QoSMaxRespT": 5,
            "CanDoOffloading": True
        })
      #  print("response content:", self.response.text)


    @task(2)
    def invoke_low1_service_function(self):
        self.response = self.client.post("/invoke/sieve", json={
            "QoSClass": 0,
            "QoSMaxRespT": 5,
            "CanDoOffloading": True
        })
      #  print("response content:", self.response.text)

    @task(0)
    def invoke_ha_service_function(self):
        self.response = self.client.post("/invoke/sieve", json={
            "QoSClass": 2,
            "QoSMaxRespT": 10,
            "CanDoOffloading": True
        })
      #  print("response content:", self.response.text)


class UserHighPerfService(HttpUser):
    tasks = [ServerledgeHighPerfTask]
    weight = 1
    wait_time = lambda self: random.expovariate(2)
