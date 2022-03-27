import json
import os
import pickle
import random
import time

import pandas
import pandas as pd

from locust import HttpUser, TaskSet, task, events


class ServerledgeLowTask(TaskSet):
    response = None


    @task(1)
    def invoke_low_service_function(self):
        params = {"img": "https://www.sweetanimals.org/wp-content/uploads/2019/10/pastore-tedesco.gif"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/imageclass", json={
            "Params": pickle.loads(p),
            "QoSClass": 0,
            "QoSMaxRespT": 100,
            "CanDoOffloading": True,
            "AsyncKey": ""
        })
    #    print("response content:", self.response.text)


class UserLowService(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1
    wait_time = lambda self: random.expovariate(1)

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

            if os.path.exists("default-responses.csv"):
                headers = False
            else:
                headers = True
            dt.to_csv("default-responses.csv", mode="a", header=headers)
