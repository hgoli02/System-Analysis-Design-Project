from client import PyClient as Client

client = Client()

for i in range(10):
    client.push(f'{i}', f'{i}')

results = []
for i in range(10):
    temp = client.pull()
    results.append(temp)

print(sorted(results))

for i in range(10):
    assert f'{i}' in results

print('Test passed')

