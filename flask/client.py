import os, requests
from requests import Session, Request

SAMPLE_FILE = "samples"
END_POINT = "http://127.0.0.1:5000/"

def tester_wrapper(test_func):
    def wrapper(*args, **kwargs):
        print(test_func.__name__.upper()+"\n")
        test_func(*args, **kwargs)
        print("\n"*3)
    return wrapper

@tester_wrapper
def test_clamd(samples):
    pass
    # c = clamClient("127.0.0.1", 3310)
    # for sample in samples:
        # print("-----testing file %s...."%sample)
        # with open(sample) as f:
            # chunk = f.read()
            # ret = c.stream_scan(chunk)
            # print(ret)

@tester_wrapper
def test_scan(samples):
    for sample in samples:
        print("-----testing file %s...."%sample)
        s = Session()
        req = Request("POST", END_POINT, files={'file': open(sample, 'rb')})
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
    test_scan(samples)
