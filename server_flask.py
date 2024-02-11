from flask import Flask, request
import os
import argparse
import logging
from threading import Lock
from threading import Thread
import pythonping
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
import time

app = Flask(__name__)
# queue_address = './DB/queue.txt'
queue_address = "./DB/"

metrics = PrometheusMetrics(app)
app.logger.setLevel(logging.INFO)

message_counter = Gauge("message_counter", "Number of messages in the queue")
message_counter.set(0)


REPLICA_COUNT = int(os.environ.get("REPLICA_COUNT", 2))

req_per_minute = 0
THRESHOLD = 700


# A class for handling the queue through a file
class Queue:
    def __init__(self, queue_address, reset=False):
        self.queue_address = queue_address
        if not os.path.exists(queue_address) or reset:
            with open(queue_address, "w") as f:
                pass
        self.length = 0
        self.datapointer = 0
        self.lock = Lock()

    def __len__(self):
        return self.length

    def push(self, message):
        self.lock.acquire()
        global req_per_minute
        with open(self.queue_address, "a") as f:
            app.logger.info(f"self.queue_address[8] = {self.queue_address[8]}")
            if self.queue_address[8] == "0":
                message_counter.inc()

            f.write(message + "\n")
            self.length += 1
            req_per_minute += 1
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        global req_per_minute
        if self.length <= 0:
            self.lock.release()
            return "$$"

        with open(self.queue_address, "r") as f:
            f.seek(self.datapointer)
            message = f.readline().strip()
            self.datapointer += len(message) + 1
            self.length -= 1
            req_per_minute += 1
            if self.queue_address[8] == "0":
                message_counter.dec()
            self.lock.release()
            return message


@app.route("/pull", methods=["GET"])
def get_message():
    global req_per_minute
    if req_per_minute > THRESHOLD:
        return "The Server Overloaded", 529
    queue_num = int(request.args["queue"])
    position = int(request.args["position"])
    if not (queue_num, position) in queues:
        app.logger.info(f"{queue_num, position} not in queus")
        response = "$$"
    else:

        app.logger.info(f"pointer={queues[(queue_num, position)].datapointer}")
        response = (
            "$$"
            if len(queues[(queue_num, position)]) <= 0
            else queues[(queue_num, position)].pop()
        )

    app.logger.info(f"pull returning response: {response}")
    return response


@app.route("/push", methods=["POST"])
def push_message():
    global req_per_minute
    if req_per_minute > THRESHOLD:
        return "The Server is Overloaded", 529
    data = request.get_json()

    value = data.get("value", "error")
    queue_num = int(data.get("queue", "error"))
    position = int(data.get("position", "error"))
    if value != "error":
        if not (queue_num, position) in queues:
            queues[(queue_num, position)] = Queue(
                queue_address + f"{queue_num}_{position}.txt"
            )
        queues[(queue_num, position)].push(value)
        return "OK"
    else:
        return "No message received", 400


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


def limiter(host):
    global req_per_minute
    while True:
        req_per_minute = 0
        time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server for a simple message queue")
    parser.add_argument(
        "--port", type=int, default=8890, help="Port number for the server"
    )
    parser.add_argument(
        "--queue", type=str, default="queue.txt", help="Port number for the server"
    )

    args = parser.parse_args()
    port = args.port
    queue_address += args.queue
    print(f"running on port: {port}")
    print(f"data is saved on: {queue_address}")
    queues = dict()
    # for i in range(REPLICA_COUNT):
    #     queues.append(Queue(queue_address + f"{i}.txt"))
    limiter = Thread(target=limiter, args=())
    limiter.start()
    app.run(debug=False, port=port, host="0.0.0.0", threaded=False)
