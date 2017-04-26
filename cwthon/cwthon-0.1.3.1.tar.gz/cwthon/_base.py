# -*- coding: utf-8 -*-
import json
import os
import requests
from cwthon import  _util

baseUrl = "https://api.chatwork.com/v2/"
reqHdr = {'X-ChatWorkToken': os.getenv('CW_TOKEN', "")}

def updateContactDictCache() -> dict:
    apiUrl = baseUrl + 'contacts'
    res = requests.get(url=apiUrl, headers=reqHdr)
    beforeParse = json.loads(res.text)
    return _util.listToDict(beforeParse, keyColumn='account_id')

def updateRoomDictCache() -> dict:
    apiUrl = baseUrl + 'rooms'
    res = requests.get(url=apiUrl, headers=reqHdr)
    beforeParse = json.loads(res.text)
    return _util.listToDict(beforeParse, keyColumn='room_id')