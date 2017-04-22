from __future__ import unicode_literals

import os
import io

from ..store import SparkStore


class SparkLocalFileSystemStore(SparkStore):

    def __init__(self, *args, **kwargs):
        super(SparkLocalFileSystemStore, self).__init__(*args, **kwargs)
        self.config['protocol'] = 'file'

    def read_file(self, local_path):
        with open(local_path, 'rb') as f:
            return io.BytesIO(f.read())

    def input_path(self):
        dataset_dir = self._dataset_path()
        if not os.path.exists(dataset_dir):
            return
        dirs = reversed(os.listdir(dataset_dir))
        for dir_name in dirs:
            flag_path = os.path.join(dataset_dir, dir_name, self.flag)
            if os.path.exists(flag_path):
                return os.path.join(dataset_dir, dir_name)
