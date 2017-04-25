import os
import struct

class CuteReader():
    def __init__(self, path):
        path_to_index_db = os.path.join(path, 'index.db')
        self.path = path
        self.data_db = open(os.path.join(path, 'data.db'), 'rb')
        self.index_db = open(path_to_index_db, 'rb')
        self._num_data = int(os.stat(path_to_index_db).st_size / 12)


    @property
    def num_data(self):
        return self._num_data

    def get(self, index):
        index = (index - 1) * 12
        self.index_db.seek(index)
        k, size = struct.unpack('<Qi', self.index_db.read(12))
        self.data_db.seek(k)
        byte_object = struct.unpack('<{0}s'.format(size), self.data_db.read(size))[0]
        return byte_object


    def close(self):
        self.data_db.close()
        self.index_db.close()
