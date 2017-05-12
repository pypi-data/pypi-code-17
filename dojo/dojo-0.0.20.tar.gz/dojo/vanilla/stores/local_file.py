from __future__ import absolute_import, print_function, unicode_literals

import os

from ..storage import Storage


class VanillaLocalFileStore(Storage):

    def read(self):
        with open(self.path, 'r') as f:
            return f.read().split('\n')

    def write(self, rows):
        output_path = '%s-00000-of-00001' % (self.path, )
        if 'prefix' in self.config:
            output_path = os.path.join(self.config['prefix'], output_path)
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_path, 'w') as f:
            f.write('\n'.join(rows).encode('utf-8'))
