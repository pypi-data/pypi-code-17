from . import WriteWrapper, ReadWrapper

class ChunkWriteWrapper(WriteWrapper):
    def __init__(self, sink, chunk_size, owns_sink):
        super(ChunkWriteWrapper, self).__init__(sink, owns_sink)
        self.chunk_size = chunk_size
        self._chunks = []
        self._chunks_len = 0

    def _drain(self):
        if not self._chunks:
            return
        remaining = b''.join(self._chunks)
        self._chunks = []
        self._chunks_len = 0
        while remaining:
            current = remaining[:self.chunk_size]
            remaining = remaining[self.chunk_size:]
            self._write_chunk(current)


    def close(self):
        super(ChunkWriteWrapper, self).close()

    def flush_self(self):
        self._drain()

    def _write_chunk(self, chunk):
        assert len(chunk) <= self.chunk_size
        self.sink.write(chunk)

    def write(self, chunk):
        self._chunks.append(chunk)
        self._chunks_len += len(chunk)
        lim = self.chunk_size
        if self._chunks_len >= lim:
            full_chunk = b''.join(self._chunks)
            to_write = full_chunk[:lim]
            self._chunks = [full_chunk[lim:]]
            self._chunks_len = len(self._chunks[0])
            self._write_chunk(to_write)


class ChunkReadWrapper(ReadWrapper):
    _buff = b''
    _got_eof = False
    def __init__(self, source, chunk_size, owns_source):
        super(ChunkReadWrapper, self).__init__(source, owns_source)
        self.chunk_size = chunk_size

    def _read_chunk(self):
        block = self.source.read(self.chunk_size)
        return block or b''

    def read(self, n=-1):
        if self._got_eof and not self._buff:
            return b''

        output = []
        out_len = 0

        chunk = self._buff[:n]
        self._buff = self._buff[n:]
        output.append(chunk)
        out_len = len(chunk)

        while True:
            if n > 0 and out_len >= n:
                break
            if not self._buff:
                next_chunk = self._read_chunk()
                if not next_chunk:
                    self._got_eof = True
                self._buff += next_chunk
                if not self._buff:
                    break
            if n > 0:
                delta = n - out_len
                chunk = self._buff[:delta]
                self._buff = self._buff[delta:]
            else:
                chunk = self._buff
                self._buff = b''
            out_len += len(chunk)
            output.append(chunk)

        return b''.join(output)

