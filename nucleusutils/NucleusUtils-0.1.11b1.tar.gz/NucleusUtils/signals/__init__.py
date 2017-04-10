import threading

from .sig import sig_name
from . import sig as _sig


class Signals:
    def __init__(self):
        self.handlers = []

    def add_handler(self, signals=None, context='', callback=None):
        if signals is None:
            signals = []
        handler = Handler(signals=signals, context=context, callback=callback)

        self.register_handler(handler)
        return handler

    def register_handler(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def call(self, signal, context=None, data=None, threaded=True, daemonic=True):
        if data is None:
            data = {}

        event = Signal(signal, context, data)

        called = []
        for handler in self._get_handler(signal, context):
            if threaded:
                result = handler.call_threaded(event, daemonic)
            else:
                result = handler.call(event)
            called.append(result)
        return called

    def _get_handler(self, signal, context):
        for handler in self.handlers:
            if handler.check(signal, context):
                yield handler


class Handler:
    def __init__(self, signals=None, context='', callback=None):
        if signals is None:
            signals = []
        elif not isinstance(signals, (list, set)):
            try:
                signals = list(signals)
            except TypeError:
                signals = [signals]
        self.signals = sorted(set(signals))
        self.context = context
        self.callback = callback

    def check(self, signal, context):
        ch_sig = signal in self.signals or signal < 0 or _sig.ALL in self.signals
        ch_evt = context == self.context
        if context is None:
            return ch_sig
        return ch_sig and ch_evt

    def call(self, event):
        return self.callback(event)

    def call_threaded(self, data, daemonic=True):
        thread = threading.Thread(target=self.call, args=(data,), daemon=daemonic)
        thread.start()
        return thread

    def __str__(self):
        signals = ' '.join(map(sig_name, self.signals))
        return f"[Handler at {hex(id(self))} '{self.context or '*'}' -> {signals}]"


class Signal:
    def __init__(self, signal, context, data):
        self.signal = signal
        self.context = context
        self.data = data

    def __str__(self):
        return f"[Signal at {hex(id(self))}  '{self.context or '*'}' -> {sig_name(self.signal)}]"


proc = Signals()


def add_handler(signals=None, context='', callback=None):
    return proc.add_handler(signals, context, callback)


def call(signal, context=None, data=None, threaded=True, daemonic=True):
    return proc.call(signal, context, data, threaded, daemonic)
