# -*- coding: utf-8 -*-
# author: Da Huo
# email: dh2582@nyu.edu

import os, requests, random
from locust import HttpLocust, TaskSet, task

SAMPLE_FILE = "samples"

samples = []

class UserBehavior(TaskSet):
    def on_start(self):
        self._samples = []
        for root, dirs, files in os.walk(SAMPLE_FILE):
            for filename in files:
                filepath = os.path.join(root, filename)
                self._samples.append(filepath)

    @task
    def test_scan(self):
        sample = random.choice(self._samples)
        r = self.client.post("/clam/scan", files={'file': open(sample, 'rb')})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "http://127.0.0.1:5000"
    min_wait = 5000
    max_wait = 9000
