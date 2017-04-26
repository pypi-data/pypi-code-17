# -*- coding: utf-8 -*-
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
