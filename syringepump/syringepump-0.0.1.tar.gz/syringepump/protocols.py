#!/usr/bin/env python
"""
syringepump.com basic protocol

commands:
    <command data><CR:x0D>
responses:
    <STX:x02><response><ETX:x03>


safe protocol has crc16 TODO
"""


class Basic(object):
    def format_message(self, msg):
        assert isinstance(msg, (str, unicode))
        if len(msg) and msg[-1] != '\r':
            return msg + '\r'
        return msg

    def parse_response(self, response):
        assert len(response)
        assert response[0] == '\x02'
        assert response[-1] == '\x03'
        return response[1:-1]


# class Safe(object):  TODO
