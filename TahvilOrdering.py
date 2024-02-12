### this test checks if the order garantee holds, i.e. if (k1,v1) is pushed before (k1,v2)
### then it is read before (k1,v2)

import random
import sys
from typing import Dict, List

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


TEST_SIZE = 3000
KEY_SIZE = 8
SUBSCRIER_COUNT = 1

key_seq = [random.choice(range(KEY_SIZE)) for _ in range(TEST_SIZE)]

pulled: Dict[str, List[int]] = {}
for i in range(KEY_SIZE):
    pulled[f"{i}"] = []

def validate_pull(key: str, val: str):
    next_val = int(val)
    if len(pulled[key]) != 0:
        prev_val = pulled[key][-1]
        if prev_val >= next_val:
            print(f"order violation, seq: [{prev_val}, {next_val}]\tkey: [{key}]")
            sys.exit(255)
    pulled[key].append(next_val)


for _ in range(SUBSCRIER_COUNT):
    subscribe(validate_pull)


for i in range(TEST_SIZE):
    push(f"{key_seq[i]}", f"{i}")

print("order test passed successfully!")
