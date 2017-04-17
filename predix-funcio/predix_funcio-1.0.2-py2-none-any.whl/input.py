import sys
import json
import bytes
import message

class FuncReader(object):
    def __init__(self, fileObject = sys.stdin):
        self.fileObject = fileObject

    def nextMessage(self):
        return deserializeMessage(self.fileObject)

# headers - A dict string -> list of strings
def serializeHeaders(headers):
    return bytearray(json.dumps(headers), encoding="utf-8")

# Returns - A dict string -> list of strings
def deserializeHeaders(headers):
    return json.loads(headers.decode("utf-8"), encoding="utf-8");

def serializeMessage(message):
    headerBytes = serializeHeaders(message.headers)
    allHeaderBytes = bytes.intToBytes(len(headerBytes))
    allHeaderBytes.extend(headerBytes)

    allBodyBytes = bytes.intToBytes(len(message.body))
    allBodyBytes.extend(message.body)

    allHeaderBytes.extend(allBodyBytes);
    return allHeaderBytes

def deserializeMessage(fileObject):
    numHeadersBytes = bytes.readNBytes(fileObject, 4)
    numHeaders = bytes.bytesToInt(numHeadersBytes)

    headersBytes = bytes.readNBytes(fileObject, numHeaders)
    headers = deserializeHeaders(headersBytes)

    numBodyBytes = bytes.readNBytes(fileObject, 4)
    numBody = bytes.bytesToInt(numBodyBytes)

    body = bytes.readNBytes(fileObject, numBody)

    return message.Message(headers, body)
