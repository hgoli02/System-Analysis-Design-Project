from client import PyClient as Client
import time

client = Client()

messages = []

while True:
    temp = client.pull()
    if temp == "$$":
        break
    messages.append(temp)

for m in messages:
    client.push(m, m)

