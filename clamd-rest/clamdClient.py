# -*- coding: utf-8 -*-
# author: Da Huo
# email: dh2582@nyu.edu

import socket, struct

class ClamdError(Exception):
    pass

class ConnectionError(ClamdError):
    """Class for errors communication with clamd"""

# socket context
class socket_ctx(object):
    def __init__(self, IP, port):
        self._IP = IP
        self._port = port

    def __enter__(self):
        try:
            self._fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._fd.connect((self._IP, self._port))
            return self
        except (socket.error, socket.timeout):
            raise ConnectionError

    def __exit__(self, type, value, traceback):
        self._fd.close()

    def send_cmd(self, cmd):
        try:
            cmd = str.encode("n{0}\n".format(cmd))
            return self._fd.send(cmd)
        except (socket.error, socket.timeout):
            raise ConnectionError

    def recv_cmd(self):
        try:
            raw = self._fd.recv(4096)
            decoded = bytes.decode(raw)
            return decoded
        except (socket.error, socket.timeout):
            raise ConnectionError

    # send raw stream
    #
    # @buf:
    # @off_size:
    # @length: when length is set to 0, send_stream will send the entire buffer
    # @return: bytes have been sent
    def send_stream(self, buf, off_size = 0, length = 0):
        assert (length >= 0), "length should be more than 0"
        assert (off_size >= 0), "off_size should be more than 0"
        end = len(buf)
        if length != 0:
            end = min(buf, off_size+length)
        return self._fd.send(buf[off_size: end])

class clamClient(object):
    def __init__(self, IP = "127.0.0.1", port = 3310):
        assert isinstance(IP, str), "type of IP should be a string"
        assert isinstance(port, int), "type of port should be an integer"
        self._port = port
        self._IP= IP

    # encode length as a 4 byte unsigned integer in network byte order
    @staticmethod
    def encode_len(length):
        return struct.pack("!L", length)

    def ping(self):
        with socket_ctx(self._IP, self._port) as fp:
            fp.send_cmd("PING")
            return fp.recv_cmd()

    def version(self):
        with socket_ctx(self._IP, self._port) as fp:
            fp.send_cmd("VERSION")
            return fp.recv_cmd()

    def stream_scan(self, buf):
        with socket_ctx(self._IP, self._port) as fp:
            fp.send_cmd("INSTREAM")
            sent_length = 0
            pkt_size = 4096
            while sent_length < len(buf):
                to_send = min(len(buf) - sent_length, pkt_size)
                # send <length> first
                fp.send_stream(self.encode_len(to_send))
                # send <packet> next
                ret = fp.send_stream(buf, sent_length, to_send)
                # print("%d bytes send"%ret)
                assert (to_send == ret), "send failure: sent bytes is %d, to send bytes is %d"%(ret, to_send)
                sent_length += ret
            fp.send_stream(self.encode_len(0))
            return fp.recv_cmd()

if __name__ == "__main__":
    c = clamClient(port=3312)
    ret = c.ping()
    print(ret)
    # with open("./samples/sample") as f:
        # chunk = f.read()
        # ret = c.stream_scan(chunk)
        # print(ret)
