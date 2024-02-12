from client import PyClient as Client
import time
import random

client = Client()

NUM = 1000
c = []
for i in range(NUM):
    r = random.randint(0, 1000)
    print(f"pushed ({r}, value{i + 1})")
    client.push(f'{r}', f'value{i + 1}')
    time.sleep(0.01)
    c.append(f'value{i + 1}')

l = []
for i in range(NUM // 2):
    a = client.pull()
    time.sleep(0.01)
    print(a)
    l.append(a[1])

input("enter something to continue")

for i in range(NUM // 2):
    a = client.pull()
    time.sleep(0.01)
    print(a)
    l.append(a[1])

assert sorted(l) == sorted(c)

print("Test Passed")