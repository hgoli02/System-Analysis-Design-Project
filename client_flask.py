import requests
import time
from threading import Thread

def push(url, message):
    response = requests.post(url + '/push', data=message)
    print('Received from server: ' + response.text)
    return response.text

def pull(url):
    response = requests.get(url + '/pull')
    print('Received from server: ' + response.text)
    return response.text

def subscribe_runner(url):
    while True:
        response = requests.get(url + '/pull')
        data = response.text
        if data == "no message":
            time.sleep(1)
        else:
            print('Subscribed message: ' + data)

def subscribe(url):
    thread = Thread(target=subscribe_runner, args=(url,))
    thread.start()

if __name__ == '__main__':
    server_url = 'http://127.0.0.1:8000'
    while True:
        data = input('waiting for input')
        if data == "get":
            pull(server_url)
        elif data == "subscribe":
            subscribe(server_url)
        else:
            push(server_url, data)
