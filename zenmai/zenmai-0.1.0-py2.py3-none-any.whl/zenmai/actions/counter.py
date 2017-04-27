class Counter:
    def __init__(self, i):
        self.i = i

    def __call__(self, fmt):
        i = self.i
        self.i += 1
        if fmt is None:
            return i
        else:
            return fmt.format(i)
counter = Counter
