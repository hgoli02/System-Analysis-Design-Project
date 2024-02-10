from client import PyClient as Client
import time

client = Client()
C = 5
for i in range(C):
    client.push(f'{i}', f'{i}')
    time.sleep(0.05)

results = []
for i in range(C):
    temp = client.pull()
    time.sleep(0.05)
    if temp == 'no message':
        results.append(-1)
    else:
        results.append(int(temp))

print(sorted(results))

for i in range(C):
    assert i in results

print('Test passed')


