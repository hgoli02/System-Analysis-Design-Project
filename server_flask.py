from flask import Flask, request
import os
import argparse

app = Flask(__name__)
queue_address = './DB/queue.txt'

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
        with open(self.queue_address, 'r') as f:
            return len(f.readlines())

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
            self.datapointer += len(message) + 2
            self.length -= 1
            return message

queue = Queue(queue_address, reset=True)

@app.route('/pull', methods=['GET'])
def get_message():
    response = "$$" if len(queue) <= 0 else queue.pop()
    return response

@app.route('/subscribe', methods=['GET'])
def subscribe():
    # Implement subscription logic here
    # This is a simplistic example; adjust according to your needs
    if len(queue) <= 0:
        return "No messages"
    else:
        response = queue.pop()
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
    args = parser.parse_args()
    print(f"running on port: {args.port}")
    app.run(debug=True, port=args.port, host="0.0.0.0")
