import os
import contextlib
import csv
import snappy
import smart_open
import io

class WriteWrapper(io.IOBase):
    def __init__(self, sink, owns_sink):
        self.sink = sink
        self.owns_sink = owns_sink

    def flush_self(self):
        pass

    def flush(self):
        self.flush_self()
        if hasattr(self.sink, 'flush'):
            self.sink.flush()

    def close_self(self):
        pass

    def close(self):
        self.flush()
        self.close_self()
        if self.owns_sink:
            self.sink.close()

    def write(self, chunk):
        self.sink.write(chunk)



class ReadWrapper(io.IOBase):
    def __init__(self, source, owns_source):
        self.source = source
        self.owns_source = owns_source

    def close_self(self):
        pass

    def close(self):
        self.close_self()
        if self.owns_source:
            self.source.close()

    def read(self, size=-1):
        return self.source.read(size)

