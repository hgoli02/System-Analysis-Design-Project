import requests
import time
from threading import Thread
import argparse

class PyClient:
    def __init__(self, server_url='localhost', port=8000, verbose=False):
        self.server_url = f'http://127.0.0.1:{port}' if server_url == 'localhost' else server_url
        self.verbose = verbose

    def push(self, key, value):
        message = key+','+value
        response = requests.post(self.server_url + '/push', data=message)
        if self.verbose:
            print('Received from server: ' + response.text)
        return response.text

    def pull(self):
        response = requests.get(self.server_url + '/pull')
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