import os, clamd
from flask import Flask, request

app = Flask(__name__)

@app.route('/clam/ping', methods=['GET'])
def upload_file():
    cd = clamd.ClamdNetworkSocket()
    return cd.pong

@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    f = request.files['file']
    if f:
        pdb.set_trace()
        return "upload OK!"
    return "upload file"

if __name__ == '__main__':
    app.run()
