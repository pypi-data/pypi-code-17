import hashlib
import json
import time

from Logger import *


class Hash(object):
    """docstring for Hash"""

    def __init__(self, server_key, private_key):
        self.server_key = server_key
        self.private_key = private_key

    def generateHashData(self, array_data, req):
        try:
            timestamp = int(time.time())
            hash_data = self.getHash(timestamp, array_data, req)

            dataDict = {'data': array_data, 'checksum': hash_data, 'request': req, 'timestamp': timestamp}

            reqData = json.dumps(dataDict, sort_keys=True, separators=(',', ':'))
            return reqData
        except Exception as e:
            Logger.logInfo("Error Occurred while creating Data")
            Logger.logError(e)

    def getHash(self, timestamp, array_data, req):
        try:
            jsonString = json.dumps(array_data, sort_keys=True, separators=(',', ':'))
            stringData = self.server_key + "|" + str(timestamp) + "|" + jsonString + "|" + self.private_key + "|" + req
            Logger.logInfo(stringData)
            hashString = hashlib.sha512(stringData).hexdigest()
            return hashString

        except Exception as e:
            Logger.logInfo("Hash Error")
            Logger.logError(e)
