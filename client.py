import socket
import threading
from threading import Thread
import time

def init():
    # get the hostname
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    server_address = ('127.0.0.1', 8888)
    client_socket.connect(server_address)

    return client_socket

def push(client_socket, message):
    client_socket.send(message.encode('utf-8'))
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)
    return data

def pull(client_socket):
    client_socket.send("get".encode())
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)
    return data

def subscribe_runner(host, port):
    sub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub_socket.connect((host, port))
    print("Connected to server")
    while True:
        sub_socket.send("subscribe".encode())
        data = sub_socket.recv(1024).decode()
        if data == "No messages":
            time.sleep(1)
        else:
            print(data)

def subscribe(host, port):
    #create a Thread
    #subscribe to server and listen for messages
    #print messages as they come in
    #if message is "quit", then close connection
    #Create a new Thread (just do it)

    thread = Thread(target = subscribe_runner, args = (host, port,))
    thread.start()

    

if __name__ == '__main__':
    client_socket = init()
    while True:
        data = input(' -> ')
        if data == "get":
            pull(client_socket)
        elif data == "subscribe":
            subscribe('127.0.0.1', 8888)
        else:
            push(client_socket, data)
    client_socket.close()  # close the connection