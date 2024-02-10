from client import PyClient as Client
import time
import threading


NUM = 10
CLIENTS = 1000
clients = []
final_results = {}
final_pushed = {}

for i in range(CLIENTS):
    clients.append(Client())

def client_runner(client, id):
    pushed = []
    for i in range(NUM):
        client.push(f"c{id}", f"v{i}+{id}")
        pushed.append(f"v{i}+{id}")
    final_pushed[id] = pushed
    

    results = []
    for i in range(NUM):
        temp = client.pull()
        results.append(temp)

    final_results[id] = results
    

start_time = time.time()
threads = []
for i in range(CLIENTS):
    threads.append(threading.Thread(target=client_runner, args=(clients[i], i)))

for i in range(CLIENTS):
    threads[i].start()

for i in range(CLIENTS):
    threads[i].join()

end_time = time.time()

print(f"Time taken: {end_time - start_time}")
final = []
target = []
for i in range(CLIENTS):
    final += final_results[i]
    target += final_pushed[i]

print(len(final))
print(len(target))
print(sorted(final)[:20])
print(sorted(target)[:20])
print(sorted(final) == sorted(target))

