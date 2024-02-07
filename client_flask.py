import requests
import time
from threading import Thread
import argparse

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
    parser = argparse.ArgumentParser(description='Client for a simple message queue')
    parser.add_argument('--server_url', type=str ,help='The URL of the server', default='localhost')
    parser.add_argument('--port', type=int, default=8000, help='Port number for the server')
    args = parser.parse_args()
    server_url = 'http://127.0.0.1:'+str(args.port) if args.server_url == 'localhost' else args.server_url 
    while True:
        data = input('waiting for input: \n')
        if data == "get":
            pull(server_url)
        elif data == "subscribe":
            subscribe(server_url)
        else:
            push(server_url, data)
