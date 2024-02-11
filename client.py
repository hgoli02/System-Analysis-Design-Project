import requests
import time
from threading import Thread
import argparse
import random

class PyClient:
    def __init__(self, server_url='localhost', port=8000, verbose=False):
        self.server_url = f'http://127.0.0.1' if server_url == 'localhost' else server_url
        self.verbose = verbose
        self.port = port

    def get_url(self):
        if (random.random() > 0.5):
            return self.server_url + ':' + str(self.port)
        else:
            return self.server_url + ':' + str(self.port)

    def push(self, key, value):
        message = key+','+value
        response = requests.post(self.get_url() + '/push', data=message)
        if self.verbose:
            print('Received from server: ' + response.text)
        return response.text

    def pull(self):
        response = requests.get(self.get_url() + '/pull')
        if self.verbose:
            print('Received from server: ' + response.text)
        return response.text

    def subscribe_runner(self, url, f):
        while True:
            response = requests.get(url + '/pull')
            data = response.text
            if data == "no message":
                time.sleep(1)
            else:
                f(data)

    def subscribe(self, f):
        thread = Thread(target=self.subscribe_runner, args=(self.server_url, f))
        thread.start()