import random

from locust import HttpUser, TaskSet, task


class OpenWhiskTask(TaskSet):
    response = None

    @task(1)
    def invoke_sieve_function(self):
        self.response = self.client.get("/sieve")
        print("response content:", self.response.text)


class UserOpenWhiskService(HttpUser):
    tasks = [OpenWhiskTask]
    weight = 1
    wait_time = lambda self: random.expovariate(2)

# /bin/bash openwhisk-test.sh -p 1234 -h "http://34.151.90.112:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502" -u 100
