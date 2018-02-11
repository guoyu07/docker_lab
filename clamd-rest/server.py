# -*- coding: utf-8 -*-
# author: Da Huo
# email: dh2582@nyu.edu

import os, socket, json, pdb
from clamd import ClamdNetworkSocket, ConnectionError, BufferTooLongError
from flask import Flask, request

from gevent.monkey import patch_all
patch_all()

app = Flask(__name__)

# HOST = "127.0.0.1"
# PORT = 3310
HOST = os.environ["CLAMD_HOST"]
PORT = int(os.environ["CLAMD_PORT"])

class Msg(object):
    def __init__(self):
        self.msg = None

    def to_string(self):
        return json.dumps(self.__dict__)


@app.route('/clam/ping', methods=['GET'])
def ping():
    ret = Msg()
    try:
        c = ClamdNetworkSocket(HOST, PORT)
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
            c = ClamdNetworkSocket(HOST, PORT)
            ret.msg = c.instream(f.stream)
        except ConnectionError:
            ret.msg = "connection error"
        except BufferTooLongError:
            ret.msg = "buffer too long"
    return ret.to_string()

if __name__ == '__main__':
    app.run()
