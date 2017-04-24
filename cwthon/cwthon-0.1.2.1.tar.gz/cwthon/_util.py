# -*- coding: utf-8 -*-
from types import *

def getStr(target) -> str:
    targetType = type(target)
    if targetType is UnicodeType:
        return target.encode('utf-8')
    elif targetType is StringType:
        return target
    elif targetType is IntType:
        return str(target)

def listToDict(list : list , keyColumn : str) -> dict:
    parsed = dict()
    for item in list :
        key = item.get(keyColumn)
        parsed.update({key : item})

    return parsed

def replaceParam(target : str, params : dict) -> str:
    for key in params.keys() :
        value = params[key]
        replaceKey = '{' + key +'}'
        if value and replaceKey:
            target = target.replace(replaceKey, str(value))
    return target
