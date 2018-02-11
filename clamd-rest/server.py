# -*- coding: utf-8 -*-
# author: Da Huo
# email: dh2582@nyu.edu

import os, socket, json, redis, hashlib
from clamdClient import clamClient, ConnectionError
from flask import Flask, request

from gevent import wsgi
from gevent.monkey import patch_all
patch_all()


# CLAMD_HOST = "127.0.0.1"
# CLAMD_PORT = 3310
CLAMD_HOST = os.environ["CLAMD_HOST"]
CLAMD_PORT = int(os.environ["CLAMD_PORT"])

# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])

app = Flask(__name__)
redis_pool = redis.ConnectionPool(host = REDIS_HOST , port = REDIS_PORT)

class Msg(object):
    def __init__(self):
        self.msg = None

    def to_string(self):
        return json.dumps(self.__dict__)

@app.route('/clam/ping', methods=['GET'])
def ping():
    ret = Msg()
    try:
        c = clamClient(CLAMD_HOST, CLAMD_PORT)
        ret.msg = c.ping()
    except ConnectionError:
        ret.msg = "connection error"
    return ret.to_string()


@app.route('/clam/scan', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    ret = Msg()
    if 'file' not in request.files:
        ret.msg = "no file part"
    else:
        f = request.files["file"]
        try:
            r = redis.Redis(connection_pool = redis_pool) 
            data = f.stream.read()
            file_hash = hashlib.md5(data).hexdigest()
            if r.exists(file_hash):
                ret.msg = r.get(file_hash)
            else:
                c = clamClient(CLAMD_HOST, CLAMD_PORT)
                ret.msg = c.stream_scan(data)
                r.set(file_hash, ret.msg, ex=60)
        except ConnectionError:
            ret.msg = "connection error"
    return ret.to_string()

if __name__ == '__main__':
    server = wsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
