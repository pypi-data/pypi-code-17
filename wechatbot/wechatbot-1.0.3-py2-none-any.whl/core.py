# -*- coding:utf-8 -*-
from wechatbot import r


def parse_command(text):
    if text.startswith('!'):
        if ' ' in text:
            command, command_string = text[1:].split(' ', 1)
            return r.call_method(command, command_string)
        else:
            return r.call_method(text[1:])
