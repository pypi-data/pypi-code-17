# -*- coding: utf-8 -*-

import _utils


class Encoder(object):
    def __init__(self):
        self.filename = None
        return

    def set_filename(self, filename):
        self.filename = filename
        return

    def encode(self):
        raise NotImplementedError

    def Encode(self):
        buff = _utils.StdoutToBuffer(self.encode)
        if self.filename:
            open(self.filename, 'w').write(buff)
        return buff
