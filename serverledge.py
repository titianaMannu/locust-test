import json
import os
import pickle
import random
import time

import pandas as pd
from locust import HttpUser, TaskSet, task, events


class ServerledgeHighPerfTask(TaskSet):
    response = None

    @task(1)
    def invoke_hp1_service_function(self):
        params = {"n": "1000"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/fib", json={
            "Params": pickle.loads(p),
            "QoSClass": 1,
            "QoSMaxRespT": 1.5,
            "CanDoOffloading": True,
            "AsyncKey": ""
        })
        # print("response content:", self.response.text)

    @task(2)
    def invoke_low1_service_function(self):
        params = {"n": "1000"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/fib", json={
            "Params": pickle.loads(p),
            "QoSClass": 0,
            "QoSMaxRespT": 15,
            "CanDoOffloading": True,
            "AsyncKey": ""
        })
        # print("response content:", self.response.text)

    @task(1)
    def invoke_ha_service_function(self):
        params = {"n": "1000"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/fib", json={
            "Params": pickle.loads(p),
            "QoSClass": 2,
            "QoSMaxRespT": 10,
            "CanDoOffloading": True,
            "AsyncKey": ""
        })
    # print("response content:", self.response.text)


class UserHighPerfService(HttpUser):
    tasks = [ServerledgeHighPerfTask]
    weight = 1
    wait_time = lambda self: random.expovariate(3)

    @events.request.add_listener
    def my_request_handler(request_type, name, response_time, response_length, response,
                           context, exception, start_time, url, **kwargs):
        if exception:
            print(f"Request to {name} failed with exception {exception}")
        else:
            print(f"Successfully made a request to: {name}")
            dict = json.loads(response.text)
            dict["time"] = time.time()
            # print(dict)
            dt = pd.DataFrame(dict, index=[0])

            if os.path.exists("reports/serverledge-responses.csv"):
                headers = False
            else:
                headers = True
            dt.to_csv("serverledge-responses.csv", mode="a", header=headers)
