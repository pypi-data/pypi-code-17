_index = 0
_name = __name__.split('.')[-1]


def next_sig():
    global _index
    _index += 1
    return _index - 1


def sig_name(sig):
    signals = filter(lambda var: var[0].isupper(), globals().items())
    for name, signal in signals:
        if sig == signal:
            return _name + '.' + name + ':' + str(sig)
    return _name + ':' + str(sig)


ALL = -1
BASE = next_sig()
EVENT = next_sig()

CREATE = next_sig()
INIT = next_sig()
SETUP = next_sig()
START = next_sig()
ADD = next_sig()
APPEND = next_sig()
UPDATE = next_sig()
POP = next_sig()
REMOVE = next_sig()
DELETE = next_sig()
STOP = next_sig()
KILL = next_sig()
EXIT = next_sig()

CALL = next_sig()
TRIGGER = next_sig()
