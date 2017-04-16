# -*- coding:utf-8 -*-
from wechatbot.exc import (
    BotSystemException,
    BotErrorCode
)


class Routing(object):

    def __init__(self):
        self.func_map = {}

    def register(self, routing_key):
        def func_wrapper(func):
            if routing_key in self.func_map:
                raise BotSystemException(BotErrorCode)
            self.func_map[routing_key] = func
            return func
        return func_wrapper

    def call_method(self, command=None, *args, **kwargs):
        """Call method by command and msg

        :param command: the command you registered
        :param args:  the msg you passed on
        :param kwargs:
        :return:
        """
        return self.func_map[command](*args, **kwargs)


r = Routing()
