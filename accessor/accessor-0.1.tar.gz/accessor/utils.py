# -*- coding: utf-8 -*-


def indexgetter(bit):
    def fnc(obj):
        return obj[int(bit)]
    return fnc
