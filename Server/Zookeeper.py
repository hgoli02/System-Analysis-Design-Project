from flask import Flask, request
import os
import random
import hashlib 

app = Flask(__name__)
queue_address = './DB/queue.txt'

list_nodes = [("localhost", "8890"), ("localhost", "8891"), ("localhost", "8892")] # should get from docker_env

def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

@app.route('/get_node', methods=['GET'])
def get_node():
    key = request.data.decode('utf-8')
    hash = int(sha256(key),base=16) % len(list_nodes)
    return hash

if __name__ == "__main__":
    app.run(debug=True, port=8899, host="0.0.0.0")
