import requests

from Hash import *
from Logger import *


class HTTPInterface:
    def __init__(self, server_key, private_key, base_url):
        self.server_key = server_key
        self.private_key = private_key
        self.base_url = base_url
        self.hashObject = Hash(self.server_key, self.private_key)

    def getHash(self, array_data, req):
        try:
            hashedData = self.hashObject.generateHashData(array_data, req)
            return hashedData
        except Exception as e:
            Logger.logInfo("Some Error Occured while encryption")
            Logger.logError(e)

    def getHeaders(self):
        headers = {
            'X-ServerKey': self.server_key,
            'Content-type': 'application/json'
        }
        return headers

    @staticmethod
    def sendRequestHelper(url, mData, req_headers, method):
        try:
            if method == "POST":
                Logger.logInfo(mData)
                response = requests.post(url, data=mData, headers=req_headers)
            else:
                response = requests.get(url, data=mData, headers=req_headers)

            return response
        except Exception as e:
            raise e

    def sendRequest(self, subURL, mData, method):
        try:
            req_headers = self.getHeaders()
            url = self.base_url + subURL
            return self.sendRequestHelper(url, mData, req_headers, method)
        except Exception as e:
            Logger.logInfo("Some Send Req Occured")
            Logger.logError(e)

    def send(self, req, array_data, subURL, method="POST"):
        try:
            mData = self.getHash(array_data, req)
            result = self.sendRequest(subURL, mData, method)
            return (result.status_code, result.text)
        except Exception as e:
            Logger.logInfo("Some Error Occured")
            Logger.logError(e)
            return ("400", "Some Error Occured")
