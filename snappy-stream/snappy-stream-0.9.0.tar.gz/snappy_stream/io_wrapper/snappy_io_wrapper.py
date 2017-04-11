import snappy
from . import WriteWrapper, ReadWrapper
from .chunk_io_wrapper import ChunkWriteWrapper, ChunkReadWrapper


class SnappyWriteStreamCore(WriteWrapper):
    _compressor_instance = None

    @property
    def _compressor(self):
        if self._compressor_instance is None:
            self._compressor_instance = snappy.StreamCompressor()
        return self._compressor_instance

    def write(self, chunk):
        compressed = self._compressor.add_chunk(chunk)
        self.sink.write(compressed)


class SnappyConsts(object):
    MAX_CHUNK = 65535 # 64kb
    ONE_MB = 1024 * 1024
    TEN_MB = ONE_MB * 10



class SnappyWriteWrapper(WriteWrapper):
    def __init__(self, sink, owns_sink, chunk_size=SnappyConsts.MAX_CHUNK):
        super(SnappyWriteWrapper, self).__init__(
            ChunkWriteWrapper(
                sink=SnappyWriteStreamCore(sink, owns_sink=owns_sink),
                chunk_size=chunk_size,
                owns_sink=True
            ),
            owns_sink=True
        )



class SnappyReadStreamCore(ReadWrapper):
    _decompressor_instance = None

    @property
    def _decompressor(self):
        if self._decompressor_instance is None:
            self._decompressor_instance = snappy.StreamDecompressor()
        return self._decompressor_instance

    def read(self, n=-1):
        buff = self.source.read(n)
        if not buff:
            return buff
        return self._decompressor.decompress(buff)


class SnappyReadWrapper(ReadWrapper):
    def __init__(self, source, owns_source, chunk_size=SnappyConsts.MAX_CHUNK):
        super(SnappyReadWrapper, self).__init__(
            ChunkReadWrapper(
                source=SnappyReadStreamCore(source, owns_source=owns_source),
                chunk_size=chunk_size,
                owns_source=True
            ),
            owns_source=True
        )

