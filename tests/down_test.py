from client import PyClient as Client
import time
import random

client = Client()

print(client.push(f'key{random.randint}', 'value1'))
print(client.push(f'key{random.randint}', 'value2'))
print(client.push(f'key{random.randint}', 'value3'))
print(client.push(f'key{random.randint}', 'value4'))
print(client.push(f'key{random.randint}', 'value5'))
print(client.push(f'key{random.randint}', 'value6'))
print(client.push(f'key{random.randint}', 'value7'))
print(client.push(f'key{random.randint}', 'value8'))
print(client.push(f'key{random.randint}', 'value9'))
print(client.push(f'key{random.randint}', 'value10'))
print(client.push(f'key{random.randint}', 'value11'))
print(client.push(f'key{random.randint}', 'value12'))

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
