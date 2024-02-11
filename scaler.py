from client import PyClient as Client
import time

client = Client()

messages = []

#pull until empty
while True:
    temp = client.pull()
    if temp == None:
        break
    messages.append(temp)