# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from maui.field import Field
from collections import deque


class ObjectSwapper(object):

    def __init__(self, object_list):

        self.__objects = deque(object_list)
        self.__pointer = deque()

        if isinstance(object_list[0], Field):
            for el in self.__objects:
                self.__pointer.append(el.d)
            self.__swap_fields = True
        else:
            self.__pointer = self.__objects
            self.__swap_fields = False

    def __getitem__(self, item):
        return list(self.value)[item]

    @property
    def value(self):
        if self.__swap_fields:
            ret = deque()
            for k, el in enumerate(self.__objects):
                el.d = self.__pointer[k]
                ret.append(el)
            return ret
        else:
            return self.__pointer

    def swap(self):
        tmp = self.__pointer.pop()
        self.__pointer.appendleft(tmp)

