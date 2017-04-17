# -*- coding: utf-8 -*-

class DecodeError(Exception):
    def __init__(self, context, string):
        super(DecodeError, self).__init__('%s:%s:%s: %s' % (context.filename, context.lineno+1, context.cursor, string))
        return

