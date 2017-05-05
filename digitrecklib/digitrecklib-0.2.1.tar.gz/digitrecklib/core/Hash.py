import hashlib
import json
import time

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
            print("Error Occurred while creating Data")
            print(str(e))

    def getHash(self, timestamp, array_data, req):
        try:
            jsonString = json.dumps(array_data, sort_keys=True, separators=(',', ':'))
            stringData = self.server_key + "|" + str(timestamp) + "|" + jsonString + "|" + self.private_key + "|" + req
            hashString = hashlib.sha512(stringData).hexdigest()
            return hashString

        except Exception as e:
            print("Hash Error")
            print(str(e))
