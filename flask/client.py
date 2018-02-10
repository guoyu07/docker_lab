import os, requests
from clamdClient import clamClient, ConnectionError
from requests import Session, Request

SAMPLE_FILE = "samples"
SCAN_ENDPOINT = "http://127.0.0.1:5000/clam/scan"
PING_ENDPOINT = "http://127.0.0.1:5000/clam/ping"

HOST = "127.0.0.1"
PORT = 3311

def tester_wrapper(test_func):
    def wrapper(*args, **kwargs):
        print(test_func.__name__.upper()+"\n")
        try:
            test_func(*args, **kwargs)
        except ConnectionError as e:
            print(e)
        print("\n"*2)
    return wrapper


@tester_wrapper
def test_clamd(samples):
    c = clamClient(HOST, PORT)
    for sample in samples:
        print("-----testing file %s...."%sample)
        with open(sample) as f:
            chunk = f.read()
            ret = c.stream_scan(chunk)
            print(ret)


@tester_wrapper
def test_ping():
    s = Session()
    req = Request("GET", PING_ENDPOINT)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print("response header:" + str(resp.headers) + "\n")
    print("response body:" + resp.text + "\n")


@tester_wrapper
def test_scan(samples):
    for sample in samples:
        print("-----testing file %s...."%sample)
        s = Session()
        req = Request("POST", SCAN_ENDPOINT, files={'file': open(sample, 'rb')})
        prepped = s.prepare_request(req)
        print("request header:" + str(prepped.headers) + "\n")
        resp = s.send(prepped)
        print("response header:" + str(resp.headers) + "\n")
        print("response body:" + resp.text + "\n")


if __name__ == "__main__":
    samples = []
    for root, dirs, files in os.walk(SAMPLE_FILE):
        for filename in files:
            filepath = os.path.join(root, filename)
            samples.append(filepath)
    test_clamd(samples)
    test_ping()
    test_scan(samples)
