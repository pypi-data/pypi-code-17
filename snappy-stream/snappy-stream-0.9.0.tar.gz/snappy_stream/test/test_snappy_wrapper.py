import unittest
from ..io_wrapper.snappy_io_wrapper import SnappyReadWrapper, SnappyWriteWrapper
from ..io_wrapper import ReadWrapper, WriteWrapper
from contextlib import contextmanager
from six import StringIO, BytesIO
import string

class LotsOfText(object):
    _data = None

    @property
    def data(self):
        return ''.join([string.ascii_letters] * 64)

    def __getitem__(self, item):
        return self.data.__getitem__(item)

class LotsOfBytes(object):
    _data = None

    @property
    def data(self):
        return ''.join([string.ascii_letters] * 64).encode('utf8')

    def __getitem__(self, item):
        return self.data.__getitem__(item)

@contextmanager
def restore_pos(buff, new_pos=0):
    pos = buff.tell()
    buff.seek(new_pos)
    try:
        yield
    finally:
        buff.seek(pos)


def read_all_decomp(buff):
    with restore_pos(buff):
        return SnappyReadWrapper(buff, owns_source=False).read()



class CloseTrackReader(ReadWrapper):
    was_closed = False
    def close_self(self):
        self.was_closed = True

class CloseTrackWriter(WriteWrapper):
    was_closed = False
    def close_self(self):
        self.was_closed = True


class TestBasic(unittest.TestCase):
    def test_read_to_write(self):
        buff = BytesIO()
        write_wrap = SnappyWriteWrapper(buff, owns_sink=False, chunk_size=16)
        read_wrap = SnappyReadWrapper(buff, owns_source=False)
        data = LotsOfBytes()
        original = data[:512]
        write_wrap.write(original)
        write_wrap.flush()
        self.assertTrue(buff.tell() > 0)
        buff.seek(0)
        result = read_wrap.read()
        self.assertEqual(original, result)

    def test_flush_on_end(self):
        buff = BytesIO()
        data = LotsOfBytes()
        write_wrap = SnappyWriteWrapper(buff, owns_sink=False, chunk_size=128)
        original = data[:157]
        with write_wrap as fout:
            fout.write(original)
        with restore_pos(buff, 0):
            self.assertEqual(original, SnappyReadWrapper(buff, False).read())

    def test_exact_block_multiple(self):
        buff = BytesIO()
        original = LotsOfBytes()[:256]
        with SnappyWriteWrapper(buff, owns_sink=False, chunk_size=128) as fout:
            fout.write(original)
        with restore_pos(buff, 0):
            self.assertEqual(original, SnappyReadWrapper(buff, False).read())

    def test_less_than_one_block(self):
        buff = BytesIO()
        original = LotsOfBytes()[:40]
        with SnappyWriteWrapper(buff, False, chunk_size=128) as fout:
            fout.write(original)
        with restore_pos(buff, 0):
            self.assertEqual(original, SnappyReadWrapper(buff, False).read())

    def test_write_nothing(self):
        buff = BytesIO()
        with SnappyWriteWrapper(buff, False, chunk_size=128) as fout:
            pass
        self.assertEqual(0, buff.tell())

    def test_read_empty(self):
        buff = BytesIO()
        with SnappyReadWrapper(buff, False, chunk_size=128) as fin:
            self.assertEqual(b"", fin.read())

    def test_simple_read(self):
        original = LotsOfBytes()[:1024]
        buff = BytesIO()
        with SnappyWriteWrapper(buff, False, chunk_size=128) as fout:
            fout.write(original)
        buff.seek(0)
        with SnappyReadWrapper(buff, False, chunk_size=128) as fin:
            result = fin.read()
        self.assertEqual(original, result)





class TestWriterClosing(unittest.TestCase):

    @contextmanager
    def _check_written_is_same(self):
        buff = BytesIO()
        data = LotsOfBytes()
        original = data[:157]
        yield buff, original
        self.assertEqual(original, read_all_decomp(buff))


    @contextmanager
    def _check_closed_status(self, expected):
        with self._check_written_is_same() as args:
            buff, block = args
            write_track = CloseTrackWriter(buff, owns_sink=False)
            yield write_track, block
            self.assertEqual(expected, write_track.was_closed)

    def test_close_write_1(self):
        with self._check_closed_status(True) as args:
            buff, block = args
            with SnappyWriteWrapper(buff, chunk_size=128, owns_sink=True) as fout:
                fout.write(block)

    def test_close_write_2(self):
        with self._check_closed_status(True) as args:
            buff, block = args
            fout = SnappyWriteWrapper(buff, chunk_size=128, owns_sink=True)
            fout.write(block)
            fout.close()

    def test_close_write_not_owner_1(self):
        with self._check_closed_status(False) as args:
            buff, block = args
            with SnappyWriteWrapper(buff, chunk_size=128, owns_sink=False) as fout:
                fout.write(block)

    def test_close_write_not_owner_2(self):
        with self._check_closed_status(False) as args:
            buff, block = args
            fout = SnappyWriteWrapper(buff, chunk_size=128, owns_sink=False)
            fout.write(block)
            fout.flush()
            fout.close()



class TestReaderClosing(unittest.TestCase):
    def _get_data(self, num):
        buff = BytesIO()
        with SnappyWriteWrapper(buff, owns_sink=False, chunk_size=128) as fout:
            fout.write(LotsOfBytes()[:num])
        buff.seek(0)
        return buff

    @contextmanager
    def _check_closed_status(self, num_bytes, expected):
        tracker = CloseTrackReader(self._get_data(num_bytes), owns_source=False)
        yield tracker
        self.assertEqual(expected, tracker.was_closed)

    def test_close_read_1(self):
        with self._check_closed_status(1024, True) as src:
            with SnappyReadWrapper(src, owns_source=True) as fin:
                data = fin.read()
                self.assertTrue(len(data) >= 1024)

    def test_close_read_2(self):
        with self._check_closed_status(1024, True) as src:
            fin = SnappyReadWrapper(src, owns_source=True)
            self.assertTrue(len(fin.read()) >= 1024)
            fin.close()

