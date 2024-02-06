from flask import Flask, request
import os
import argparse
import logging

app = Flask(__name__)
# queue_address = './DB/queue.txt'
queue_address = './DB/'

app.logger.setLevel(logging.INFO)

# A class for handling the queue through a file
class Queue:
    def __init__(self, queue_address, reset=False):
        self.queue_address = queue_address
        if not os.path.exists(queue_address) or reset:
            with open(queue_address, 'w') as f:
                pass
        self.length = 0
        self.datapointer = 0

    def __len__(self):
        return self.length

    def push(self, message):
        with open(self.queue_address, 'a') as f:
            f.write(message + '\n')
            self.length += 1

    def pop(self):
        if self.length <= 0:
            return "No messages"

        with open(self.queue_address, 'r') as f:
            f.seek(self.datapointer)
            message = f.readline().strip()
            self.datapointer += len(message) + 1
            self.length -= 1
            return message



@app.route('/pull', methods=['GET'])
def get_message():
    response = "$$" if len(queue) <= 0 else queue.pop()

    app.logger.info(f"pull returning response: {response}")
    return response

@app.route('/push', methods=['POST'])
def push_message():
    message = request.data.decode('utf-8')
    if message:
        queue.push(message)
        return "OK"
    else:
        return "No message received", 400

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for a simple message queue')
    parser.add_argument('--port', type=int, default=8891, help='Port number for the server')
    parser.add_argument('--queue', type=str, default='queue.txt', help='Port number for the server')

    args = parser.parse_args()
    port = args.port
    queue_address += args.queue
    print(f"running on port: {port}")
    print(f"data is saved on: {queue_address}")
    queue = Queue(queue_address, reset=True)
    app.run(debug=False, port=port, host="0.0.0.0")
