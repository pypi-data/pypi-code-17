import os
import struct

class CuteWriter():
    def __init__(self, path):
        os.mkdir(path)
        self.data_db = open(os.path.join(path, 'data.db'), 'wb')
        path_to_index_db = os.path.join(path, 'index.db')
        self.index_db = open(path_to_index_db, 'wb')

    def write(self, byte_object):
        if not (isinstance(byte_object, str) or isinstance(byte_object, bytes)):
            raise TypeError('only accept str or bytes object')

        begin = self.data_db.tell()
        self.index_db.write(struct.pack('<Qi', begin, len(byte_object)))
        self.data_db.write(struct.pack('<%ss' %(len(byte_object)), byte_object))


    def close(self):
        self.data_db.close()
        self.index_db.close()
