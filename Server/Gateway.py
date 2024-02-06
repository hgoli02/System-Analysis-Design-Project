from flask import Flask, request
import os
import random
import hashlib 
import requests

app = Flask(__name__)

list_nodes = [("localhost", "8890"), ("localhost", "8891"), ("localhost", "8892")] # should get from docker_env



def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

@app.route('/push', methods=['POST'])
def push():
    data = request.data.decode('utf-8')
    key, value = data.split(',')
    app.logger.debug(f"Body is: {data}")
    hash = int(sha256(key),base=16) % len(list_nodes)
    url = list_nodes[hash] + ":" + list_nodes[hash]
    response = requests.get(url + "/push", data=value)
    return response





if __name__ == "__main__":
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    app.run(debug=True, port=8000, host="0.0.0.0", threaded=True)
