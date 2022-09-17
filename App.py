import logging
import socket
from codeitsuisse import app
import time

import redis
from flask import Flask
logger = logging.getLogger(__name__)
app.config["DEBUG"] = True
cache = redis.Redis(host='redis', port=23946)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/', methods=['GET','POST'])
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
def default_route():
    return "Python Template"


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)
