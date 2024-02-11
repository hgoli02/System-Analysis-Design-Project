from client import PyClient as Client
import time
import threading


NUM = 10
CLIENTS = 1
clients = []
final_results = {}
final_pushed = {}

for i in range(CLIENTS):
    clients.append(Client())

def push_runner(client, id):
    pushed = []
    for i in range(NUM):
        client.push(f"c{id}", f"v{i}+{id}")
        pushed.append(f"v{i}+{id}")
    final_pushed[id] = pushed
    
def pull_runner(client, id):
    results = []
    for i in range(NUM):
        temp = client.pull()
        results.append(temp)

    final_results[id] = results

    

start_time = time.time()
threads_push = []
threads_pull = []
for i in range(CLIENTS):
    threads_push.append(threading.Thread(target=push_runner, args=(clients[i], i)))
    threads_pull.append(threading.Thread(target=pull_runner, args=(clients[i], i)))

for i in range(CLIENTS):
    threads_push[i].start()

for i in range(CLIENTS):
    threads_push[i].join()

for i in range(CLIENTS):
    threads_pull[i].start()

for i in range(CLIENTS):
    threads_pull[i].join()

end_time = time.time()

print(f"Time taken: {end_time - start_time}")
final = []
target = []
for i in range(CLIENTS):
    final += final_results[i]
    target += final_pushed[i]

print(len(final))
print(len(target))
print(sorted(final)[:100])
print(sorted(target)[:100])
print(sorted(final) == sorted(target))

#how many out of all targets are similar
for i in range(len(target)):
    if target[i] not in final:
        print(f"Not found {target[i]}")
        


