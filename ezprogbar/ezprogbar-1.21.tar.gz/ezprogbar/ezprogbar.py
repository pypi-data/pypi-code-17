from __future__ import print_function
import sys, time

class ProgressBar:
    """
    Example:
    pb = ProgressBar(n)
    for i in range(n):
        do_some_action()
        pb.advance()
    """

    def __init__(self, size, **opt):
        prompt = opt.get('prompt', 'Progress: ')
        self.size = size
        self.unit = size / 100.0
        self.percent = -1
        self.index = 0
        self.done = False
        self.start = time.time()
        self.text = '\r' + prompt + '%d%%   '
        self.callback = opt.get('callback', None)

    def advance(self, n=None):
        if self.done:
            return
        if n is None:
            self.index += 1
        else:
            self.index = n

        p = int(self.index / self.unit)

        if p > self.percent:
            sys.stdout.write(self.text % p)
            sys.stdout.flush()
            self.percent = p
            self.seconds = time.time() - self.start
            if self.callback:
                self.callback(self)

        if self.index >= self.size - 1:
            sys.stdout.write((self.text + '\n') % 100)
            sys.stdout.flush()
            self.done = True
            t = time.time() - self.start
            print("Time: %.2f seconds" % t)


