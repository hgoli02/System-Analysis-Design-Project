import socket
import threading
import time
import sys
import os
import argparse

queue_address = './DB/queue.txt'
#A class for handling the queue through a file
class Queue:
    def __init__(self, queue_address, reset=False):
        self.queue_address = queue_address
        if not os.path.exists(queue_address) or reset:
            with open(queue_address, 'w') as f:
                pass
        self.length = 0
        self.datapointer = 0
        

    def __len__(self):
        with open(self.queue_address, 'r') as f:
            return len(f.readlines())
        
    def push(self, message):
        #append to the self.datapointer
        with open(self.queue_address, 'a') as f:
            f.write(message + '\n')
            self.length += 1
            
    def pop(self):
        #read the first line and shift the file
        #read at datapointer address
        if self.length <= 0:
            return "No messages"
        
        with open(self.queue_address, 'r') as f:
            f.seek(self.datapointer)
            #read until the end of the file or the next line
            message = f.readline().strip()
            self.datapointer += len(message) + 2
            self.length -= 1
            return message
            
    

def handle_client(client_socket):
    # Handle the client's request
    while True:
        request = client_socket.recv(1024)
        print(f"Received: {request.decode('utf-8')}")
        if request.decode('utf-8') == "get":
            response = "No messages" if len(queue) <= 0 else queue.pop()
            client_socket.send(response.encode('utf-8'))
        elif request.decode('utf-8') == "subscribe":
            if len(queue) <= 0:
                client_socket.send("No messages".encode('utf-8'))
                time.sleep(1)
                continue
            response = queue.pop(0)
            client_socket.send(response.encode('utf-8'))
        else:
            queue.push(request.decode('utf-8'))
            client_socket.send("OK".encode('utf-8'))

    #client_socket.close()

def start_server(port=8888, address='127.0.0.1'):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((address, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

queue = Queue(queue_address, reset=True)

if __name__ == "__main__":
    #define the parser
    parser = argparse.ArgumentParser(description='Server for the queue')
    parser.add_argument('--reset', action='store_true', help='Reset the queue', default=False)
    parser.add_argument('--port', type=int, default=8888, help='Port to listen to')
    parser.add_argument('--address', type=str, default='127.0.0.1')

    args = parser.parse_args()

    start_server(args.port, args.address)

