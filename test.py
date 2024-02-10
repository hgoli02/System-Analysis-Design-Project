from client import PyClient as Client

clients = []

#create 5 clients

for i in range(5):
    clients.append(Client())

#create a sorted benchmark for each client
true_vlaues = {}
for i in range(5):
    true_vlaues[f'key{i}'] = [f'value{j}' for j in range(5)]

#push 5 messages to each client
for i in range(5):
    for j, client in enumerate(clients):
        print(client.push(f'key{j}', f'value{i}'))


preds = {}
#pull 5 messages from each client
for i in range(5):
    for j, client in enumerate(clients):
        pred = client.pull()
        preds[f'key{j}'] = preds.get(f'key{j}', []) + [pred]

print(preds)

#test
for key in true_vlaues:
    assert true_vlaues[key] == preds[key]

print("All tests passed!")