from client import PyClient as Client

client = Client()

NUM = 501

for i in range(NUM):
    client.push(f'{i}', f'{i}')

results = []
for i in range(NUM):
    _, temp = client.pull()
    results.append(temp)

print(sorted(results))

for i in range(NUM):
    assert f'{i}' in results

print('Test passed')


