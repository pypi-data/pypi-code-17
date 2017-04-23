#!/usr/bin/env python

import threading

class Singleton:

    _instance_lock = threading.Lock()
    _instance_name = '_singleton_instance'

    def __init__(self):

        if hasattr(self.__class__, Singleton._instance_name):
            raise RuntimeError('Singleton object already initialized; use get_instance to retrieve the instance')
        else:
            with Singleton._instance_lock:
                self.__check_and_set_init()

    def __check_and_set_init(self):
        if hasattr(self.__class__, Singleton._instance_name):
            raise RuntimeError('Singleton object already initialized; use get_instance to retrieve the instance')
        else:
            setattr(self.__class__, Singleton._instance_name, self)

    @classmethod
    def get_instance(cls):
        # Note we cannot default initialize the instance here if it hasn't yet
        # been created because this class has no knowledge of the signature
        # of the parent class' constructor
        return getattr(cls, Singleton._instance_name)
