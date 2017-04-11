from __future__ import print_function
from contextlib import contextmanager, closing
from snappy_stream.io_wrapper.snappy_io_wrapper import (
    SnappyReadWrapper,
    SnappyWriteWrapper
)
from . import HAVE_SMART_OPEN, explode_if_no_smart_open


class PrivBytesOpener(object):
    @contextmanager
    def open_read(self, *args, **kwargs):
        inner_mgr = self.open_under_read(*args, **kwargs)
        with inner_mgr as in_buff:
            with SnappyReadWrapper(in_buff, owns_source=False) as user_buff:
                yield user_buff

    @contextmanager
    def open_write(self, *args, **kwargs):
        inner_mgr = self.open_under_write(*args, **kwargs)
        with inner_mgr as out_buff:
            with SnappyWriteWrapper(out_buff, owns_sink=False) as user_buff:
                yield user_buff





class PrivFSBytesOpener(PrivBytesOpener):
    @staticmethod
    def open_under_read(file_path):
        return open(file_path, 'rb')

    @staticmethod
    def open_under_write(file_path):
        return open(file_path, 'wb')


class PrivS3BytesOpener(PrivBytesOpener):
    @staticmethod
    def _smart_open(s3_uri, mode, **smart_open_kwargs):
        explode_if_no_smart_open()
        import smart_open
        return smart_open.smart_open(s3_uri, mode, **smart_open_kwargs)

    @classmethod
    def open_under_read(cls, s3_uri, **smart_open_kwargs):
        return cls._smart_open(s3_uri, 'rb', **smart_open_kwargs)

    @classmethod
    def open_under_write(cls, s3_uri, **smart_open_kwargs):
        return cls._smart_open(s3_uri, 'wb', **smart_open_kwargs)
