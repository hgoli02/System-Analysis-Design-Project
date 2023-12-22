import socket
import threading
import time

queue = []

def handle_client(client_socket):
    # Handle the client's request
    while True:
        request = client_socket.recv(1024)
        print(f"Received: {request.decode('utf-8')}")
        if request.decode('utf-8') == "get":
            response = queue.pop(0)
            client_socket.send(response.encode('utf-8'))
        elif request.decode('utf-8') == "subscribe":
            if len(queue) <= 0:
                client_socket.send("No messages".encode('utf-8'))
                time.sleep(1)
                continue
            response = queue.pop(0)
            client_socket.send(response.encode('utf-8'))
        else:
            queue.append(request.decode('utf-8'))
            client_socket.send("OK".encode('utf-8'))

    #client_socket.close()

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('127.0.0.1', 8888))

    # Listen for incoming connections
    server_socket.listen(5)
    print("Server listening on port 8888")

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()