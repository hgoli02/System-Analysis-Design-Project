from flask import Flask, request
import os
import random
import hashlib 
import requests
import logging

PORT = os.environ.get('PORT', 8000)
BROKER_PORT = os.environ.get('BROKER_PORT', 8890)
BROKER_HOST = os.environ.get('BROKER_HOST', "http://system-analysis-design-project-queue")
NUMBER_OF_BROKERS = os.environ.get('NUMBER_OF_BROKERS', 2)

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

list_nodes = []
for i in range(int(NUMBER_OF_BROKERS)):
    list_nodes.append((BROKER_HOST + "-" + str(i+1), str(BROKER_PORT)))




def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

@app.route('/push', methods=['POST'])
def push():
    data = request.data.decode('utf-8')
    key, value = data.split(',')
    hash = int(sha256(key),base=16) % len(list_nodes)
    url = list_nodes[hash][0] + ":" + list_nodes[hash][1] + "/push"
    app.logger.info(f"url is: {url}")
    app.logger.info(f"value is: {value}")

    response = requests.post(url , data=value)
    # return "1"
    
    return response.text


@app.route('/pull', methods=['GET'])
def pull():
    
    rd = random.randint(0, len(list_nodes) - 1)
    for i in range(len(list_nodes)):
        nw = (i + rd) % len(list_nodes)
        url = list_nodes[nw][0] + ":" + list_nodes[nw][1]
        response = requests.get(url + "/pull")
        app.logger.info(f"request from {url}, response: {response.text}")
        if response.text != '$$':
            return response.text
    return 'no message'

    


if __name__ == "__main__":
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    app.logger.info(f"PORT is: {PORT}")
    app.run(debug=True, port=PORT, host="0.0.0.0", threaded=True)
