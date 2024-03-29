from flask import Flask, request
import os
import random
import hashlib
import requests
import logging
import bisect
from pythonping import ping
import threading
import time
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge

PORT = int(os.environ.get("PORT", 8000))
BROKER_PORT = int(os.environ.get("BROKER_PORT", 8890))
BROKER_HOST = os.environ.get("BROKER_HOST", "http://127.0.0.1")
NUMBER_OF_BROKERS = int(os.environ.get("NUMBER_OF_BROKERS", 1))
NUMBER_OF_COPIES = int(os.environ.get("NUMBER_OF_COPIES", 1))
REPLICA_COUNT = int(os.environ.get("REPLICA_COUNT", 1))

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
metrics = PrometheusMetrics(app)

total_messages = Gauge("total_messages", "Total number of messages in the system")
total_messages.set(0)

list_nodes = []
alive_nodes = [True] * int(NUMBER_OF_BROKERS)
if BROKER_HOST == "http://127.0.0.1":
    list_nodes.append(("http://127.0.0.1", str(BROKER_PORT)))
else:
    for i in range(int(NUMBER_OF_BROKERS)):
        list_nodes.append((BROKER_HOST + "-" + str(i + 1), str(BROKER_PORT)))

hash_ring = []


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def is_alive(url):
    try:
        response = requests.get(url + "/ping", timeout=0.2)
        return True
    except Exception as e:
        app.logger.info(f"tried to ping {url} but caught error {e}")
        return False


def upadte_nodes(i):
    while True:
        alive_nodes[i] = is_alive(list_nodes[i][0] + ":" + list_nodes[i][1])
        app.logger.info(f"node {i} aliveness: {alive_nodes[i]}")
        time.sleep(10)


def construct_consistent_hashing_ring():
    num_nodes = len(list_nodes)
    for i in range(num_nodes):
        for j in range(NUMBER_OF_COPIES):
            current_hash = int(sha256(str(i) + ";" + str(j)), base=16)
            hash_ring.append([current_hash, i])
    hash_ring.sort()
    for i in range(len(hash_ring)):
        hash_ring[i][-1] = i % NUMBER_OF_BROKERS


def find_next(key, rep, do_hash=True):  # rep is in [0,REPLICA_COUNT)
    if rep < 0 or rep >= REPLICA_COUNT:
        raise ValueError(f"rep should be between{0} and {REPLICA_COUNT - 1} inclusive")
    hash = key
    if do_hash:
        hash = int(sha256(hash), base=16)
    pos = bisect.bisect_left(hash_ring, [hash, -1])
    s = set()
    for i in range(len(hash_ring)):
        ps = (pos + i) % len(hash_ring)
        s.add(hash_ring[ps][1])
        if len(s) == rep + 1:
            # while hash_ring[ps][1] == hash_ring[(ps + 1) % len(hash_ring)][1]:
            #     ps += 1
            return hash_ring[ps][1], ps


@app.route("/push", methods=["POST"])
def push():
    data = request.data.decode("utf-8")
    if len(data.split(",")) != 2:
        app.logger.info(data)
        msg = "ERROR: there should be exactly one comma (,) in the data between key and value"
        app.logger.info(msg)
        return msg
    key, value = data.split(",")
    total_messages.inc()
    for i in range(REPLICA_COUNT):
        node, ps = find_next(key, i)
        data = {"value": value,"key":key, "queue": i, "position": ps}
        url = list_nodes[node][0] + ":" + list_nodes[node][1] + "/push"
        if alive_nodes[node]:
            app.logger.info(f"replica {i} goes to {node}, {ps}")
            try:
                response = requests.post(url, json=data)
            except Exception as e:
                app.logger.info(
                    f"tried to push to f{url} with data=f{data} but caught error {e}"
                )
        app.logger.info(f"for replica {i} url is: {url}")
        app.logger.info(f"for replica {i} value is: {value}")

    return "done"  # TODO: should fix


@app.route("/pull", methods=["GET"])
def pull():
    rd = random.randint(0, len(hash_ring) - 1)
    for i in range(len(hash_ring)):
        nw = (i + rd) % len(hash_ring)
        ret = "$$"
        for j in range(REPLICA_COUNT):
            nxt, ps = find_next(hash_ring[nw][0], j, False)
            url = list_nodes[nxt][0] + ":" + list_nodes[nxt][1]
            
            data = {"queue": f"{j}", "position": ps}
            if alive_nodes[nxt]:
                app.logger.info(f"replica {j} gets from {nxt}, {ps}")
                try:
                    response = requests.get(url + "/pull", params=data)
                    if response == "$$":
                        break
                    ret = response.text
                except Exception as e:
                    app.logger.info(
                        f"tried to pull from f{url} with data=f{data} but caught error {e}"
                    )

        if ret != "$$":
            total_messages.dec()
            return ret
    return "no message"


if __name__ == "__main__":
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    app.logger.info(f"PORT is: {PORT}")
    app.logger.info(f"broker ports are : {BROKER_HOST}")
    construct_consistent_hashing_ring()
    for i in range(NUMBER_OF_BROKERS):
        t = threading.Thread(target=upadte_nodes, args=([i]))
        t.start()
    app.logger.info("hash_ring is: " + str(hash_ring))
    app.run(debug=False, port=PORT, host="0.0.0.0", threaded=False)
