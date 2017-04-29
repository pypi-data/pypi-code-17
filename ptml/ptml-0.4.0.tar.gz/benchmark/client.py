#!/usr/local/bin/python

import sys
import socket
from threading import *
import time


class struct:
    pass


def benchmarkThread(info, hits, port, cmd, bufsize):

    start = time.time()
    bytes = 0

    for i in range(0, hits):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(("127.0.0.1", port))
        s.send(cmd)

        while 1:
            rb = len(s.recv(bufsize))
            if rb == 0: break
            bytes = bytes + rb

    info.duration = time.time() - start
    info.bytes = bytes

    info = {"duration": time.time() - start, "bytes": bytes }


def benchmark(port, hits, threads, file):

    cmd = "GET /%s HTTP/1.0\r\n\r\n" % file

    thr = {}

    for i in range(0, threads):
        thr[i] = struct()
        thr[i].thread = Thread(target=benchmarkThread,
            args=(thr[i], hits/threads, port, cmd, 8192))
        thr[i].thread.start()

    for i in range(0, threads):
        thr[i].thread.join()

    bytes = reduce(lambda a, b: a + b.bytes, thr.values(), 0)
    duration = reduce(lambda a, b: a + b.duration, thr.values(), 0) / threads

    return (bytes, duration)


if __name__ == "__main__":

    if len(sys.argv) != 5:
        sys.stderr.write("usage: %s <port> <hits> <threads> <file>\n"
            % sys.argv[0])
        sys.exit(1)

    port = int(sys.argv[1])
    hits = int(sys.argv[2])
    threads = int(sys.argv[3])
    file = sys.argv[4]

    (bytes, duration) = benchmark(port, hits, threads, file)

    print "hits:\t\t%s" % hits
    print "bytes:\t\t%d" % bytes
    print "duration:\t%.3f" % duration
    print "hits/sec:\t%.3f" % (hits / duration)
    print "bytes/sec:\t%.3f" % (bytes / duration)
    print "bytes/hit:\t%.3d" % (bytes / hits)

# vim: set et sts=4 sw=4 :
