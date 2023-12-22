import socket


def init():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    return client_socket

def push(client_socket, message):
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)
    return data

def pull(client_socket):
    client_socket.send("get".encode())
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)
    return data

def subscribe(client_socket, topic):
    pass

if __name__ == '__main__':
    client_socket = init()
    while True:
        data = input(' -> ')
        if data == "get":
            pull(client_socket)
        else:
            push(client_socket, data)
    client_socket.close()  # close the connection