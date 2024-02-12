### this test checks if the cluster performance scales with the size of the cluster
### run the test and press enter untill you see a thourghput cap in the monitoring of the cluster
### manually scale up cluster 
### press enter once more and see if you have a increase in throughput rate of the cluster

import multiprocessing

TEST_SIZE = 1000 * 1000
KEY_SIZE = 8
SUBSCRIER_COUNT = 4

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



def to_infinity():
    index = 0
    while True:
        yield index
        index += 1


def push_key(key: str):
    for i in to_infinity():
        push(key, f"{i}")
        print(key, f"{i}")

subscribe(lambda key, val: ...)

if __name__ == '__main__':  


    for i in to_infinity():
        p = multiprocessing.Process(target=push_key, args=(f'{i}',))
        p.start()
        print("did it cap?")
        print("if not, press enter to increase throughput")
        print("if capped, manually scale up the cluster and press enter to see if you can increase the throughput")
        input()