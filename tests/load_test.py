from .client import PyClient as Client

client = Client()

for i in range(1000):
    client.push(f'{i}', f'{i}')

results = []
for i in range(1000):
    temp = client.pull(f'{i}')
    results.append(temp)

for i in range(1000):
    assert f'{i}' in results

print('Test passed')


