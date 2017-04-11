from contextlib import contextmanager

from snappy_stream.detail import priv_bytes_opener as _openers

@contextmanager
def open_fs_read_bytestream(fpath):
    with _openers.PrivFSBytesOpener().open_read(fpath) as user_buff:
        yield user_buff

@contextmanager
def open_fs_write_bytestream(fpath):
    with _openers.PrivFSBytesOpener().open_write(fpath) as user_buff:
        yield user_buff

@contextmanager
def open_s3_read_bytestream(s3_uri, **kwargs):
    with _openers.PrivS3BytesOpener().open_read(s3_uri, **kwargs) as user_buff:
        yield user_buff


@contextmanager
def open_s3_write_bytestream(s3_uri, **kwargs):
    with _openers.PrivS3BytesOpener().open_write(s3_uri, **kwargs) as user_buff:
        yield user_buff


