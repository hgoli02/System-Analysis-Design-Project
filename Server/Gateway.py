from flask import Flask, request
import os
import random
import hashlib 
import requests

app = Flask(__name__)

list_nodes = [("http://172.27.53.146", "8890")]#, ("localhost", "8891"), ("localhost", "8892")] # should get from docker_env



def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

@app.route('/push', methods=['POST'])
def push():
    data = request.data.decode('utf-8')
    key, value = data.split(',')
    app.logger.debug(f"Body is: {data}")
    hash = int(sha256(key),base=16) % len(list_nodes)
    url = list_nodes[hash][0] + ":" + list_nodes[hash][1]
    response = requests.post(url + "/push", data=value)
    
    return response.text


@app.route('/pull', methods=['GET'])
def pull():
    
    rd = random.randint(0, len(list_nodes) - 1)
    for i in range(len(list_nodes)):
        nw = (i + rd) % len(list_nodes)
        url = list_nodes[nw][0] + ":" + list_nodes[nw][1]
        response = requests.get(url + "/pull")
        if response != '$$':
            return response
    return 'no message'

    

    





if __name__ == "__main__":
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    app.run(debug=True, port=8000, host="0.0.0.0", threaded=True)
