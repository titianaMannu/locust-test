import pickle

from locust import HttpUser, TaskSet, task


class ServerledgeLowTask(TaskSet):
    response = None
    last_wait_time = 0

    @task(1)
    def invoke_low_service_function(self):
        params = {"a": "1", "b": "2"}
        p = pickle.dumps(params)
        self.response = self.client.post("/invoke/sieve", json={
            "Params": pickle.loads(p),
            "QoSClass": 0,
            "QoSMaxRespT": 3,
            "CanDoOffloading": False
        })
        print("response content:", self.response.text)

    def wait_time(self):
        self.last_wait_time += 1
        print("request %d" % self.last_wait_time)
        return self.last_wait_time


class UserLowService1(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1


class UserLowService2(HttpUser):
    tasks = [ServerledgeLowTask]
    weight = 1
