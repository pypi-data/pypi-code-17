#!/usr/bin/env python

import json

class AnonObj:

    def __init__(self, _dict = None, json_str = None):

        self.__is_initialized = False
        if _dict:
            self.__init__dict__(_dict)
        if json_str:
            self.__init__dict__(json.loads(json_str))


    def __init__dict__(self, _dict):
        if self.__is_initialized:
            raise RuntimeError('Anonymous object is already initialized.')
        self.__dict__ = _dict


    def __str__(self):
        return json.dumps(self.__dict__)


    def __repr__(self):
        return json.dumps(self.__dict__)
