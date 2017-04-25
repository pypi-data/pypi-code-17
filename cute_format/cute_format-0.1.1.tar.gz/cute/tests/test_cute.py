# content of test_sample.py
from cute.cute_reader import CuteReader
from cute.cute_writer import CuteWriter
import pytest
import shutil
import os

create_dir = 'tmp'

@pytest.fixture
def cute_writer():
    if os.path.exists(create_dir):
        shutil.rmtree(create_dir)
    cw = CuteWriter(create_dir)
    return cw

def test_str_object(cute_writer):
    str_object = 'a' * 1000
    cute_writer.write(str_object)
    cute_writer.close()
    cr = CuteReader('tmp')
    byte_object = cr.get(1)
    assert str_object == byte_object
    assert cr.num_data == 1

def test_byte_object(cute_writer):
    a =  1000
    b =  2000
    cute_writer.write(bytes(a))
    cute_writer.write(bytes(b))
    cute_writer.close()
    cr = CuteReader('tmp')
    assert cr.num_data == 2
    byte_object = cr.get(1)
    assert int(byte_object) == a
    byte_object = cr.get(2)
    assert int(byte_object) == b
