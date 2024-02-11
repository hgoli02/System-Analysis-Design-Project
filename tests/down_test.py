from client import PyClient as Client
import time
import random

client = Client()

print(client.push(f'{random.randint(0, 1000)}', 'value1'))
print(client.push(f'{random.randint(0, 1000)}', 'value2'))
print(client.push(f'{random.randint(0, 1000)}', 'value3'))
print(client.push(f'{random.randint(0, 1000)}', 'value4'))
print(client.push(f'{random.randint(0, 1000)}', 'value5'))
print(client.push(f'{random.randint(0, 1000)}', 'value6'))
print(client.push(f'{random.randint(0, 1000)}', 'value7'))
print(client.push(f'{random.randint(0, 1000)}', 'value8'))
print(client.push(f'{random.randint(0, 1000)}', 'value9'))
print(client.push(f'{random.randint(0, 1000)}', 'value10'))
print(client.push(f'{random.randint(0, 1000)}', 'value11'))
print(client.push(f'{random.randint(0, 1000)}', 'value12'))

print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())

input("enter something to continue")

print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())
print(client.pull())
