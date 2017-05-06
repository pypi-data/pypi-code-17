import time
from math import sin
from ezprogbar import ProgressBar

def test1():
    pb = ProgressBar(240)
    for i in range(240):
        time.sleep(0.03)
        pb.advance()


def callback(pb):
    i = pb.index
    t = pb.seconds
    p = pb.percent

    if p in [20, 45, 82]:
        print("Hi from callback: index=%d, time=%.2f seconds, percent=%d%%" % (i,t,p))

    if t > 100:
        print("This is taking too long!")

def test2():
    n = 2*10**6
    pb = ProgressBar(n, callback=callback)
    s = 0.0
    for i in range(n):
        s += 1.0/(1 + i**(2+sin(i)))
        pb.advance()

    print("Result: s = %.6f" % (s,))

test1()
test2()


