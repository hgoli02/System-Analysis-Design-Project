### this test checks fault tolerancy of the system. 
### for each component in the system do the following:
### 1. run the test
### 2. when the pop up popes, bring down an instance of the said component. 
### 3. wait for cluster to become healty again
### 4. press enter

### note that API-Gateway, External Database, ... all are components of the system and are prune to downtime
import random
from typing import List
from threading import Lock
import time

from client import PyClient as Client

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8000
CREDENTIALS = "..."

qc = Client(SERVER_ADDRESS, SERVER_PORT, verbose=False)

def pull():
    return qc.pull()

def push(key,val):
    qc.push(key,val)


def subscribe(action):
    qc.subscribe(action)
TEST_SIZE = 1000
KEY_SIZE = 8
SUBSCRIER_COUNT = 1

key_seq = [random.choice(range(KEY_SIZE)) for _ in range(TEST_SIZE)]

pulled: List[int] = []
lock = Lock()
def store(_: str, val: bytes):
    next_val = int(val)
    with lock:
        pulled.append(next_val)


for _ in range(SUBSCRIER_COUNT):
    subscribe(store)


for i in range(TEST_SIZE//2):
    push(f"{key_seq[i]}", f"{i}")

#time.sleep(5)
#print(pulled)

print("manually fail one node and wait for cluster to become healthy again")
print("press enter when cluster is healthy")
input()

for i in range(TEST_SIZE//2,TEST_SIZE):
    push(f"{key_seq[i]}", f"{i}")

time.sleep(10)
pulled.sort()
#print(pulled)

for i in range(TEST_SIZE):
    if pulled[i]!=i:
        print("DATA loss occurred")


print("Fault tolerance test passed successfully!")
