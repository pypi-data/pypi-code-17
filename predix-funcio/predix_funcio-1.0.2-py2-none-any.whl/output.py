import sys
import bytes
import input
import message

def serializeResponse(response):
    totalBytes = bytearray()

    statusCodeBytes = bytes.intToBytes(response.statusCode)
    totalBytes.extend(statusCodeBytes)

    statusBytes = bytearray(response.status)
    numStatusBytes = bytes.intToBytes(len(statusBytes))
    totalBytes.extend(numStatusBytes)
    totalBytes.extend(statusBytes)

    messageBytes = input.serializeMessage(response.message)
    totalBytes.extend(messageBytes)

    return totalBytes;

def deserializeResponse(fileObject):
    statusCodeBytes = bytes.readNBytes(fileObject, 4)
    statusCode = bytes.bytesToInt(statusCodeBytes)

    numStatusBytes = bytes.readNBytes(fileObject, 4)
    numStatus = bytes.bytesToInt(numStatusBytes)

    statusBytes = bytes.readNBytes(fileObject, numStatus)
    status = str(statusBytes)

    messagePacket = input.deserializeMessage(fileObject)
    response = message.Response(statusCode, status, messagePacket)
    return response;

class FuncWriter(object):
    def __init__(self, fileObject = sys.stdout):
        self.fileObject = fileObject

    def writeMessage(self, response):
        responseBytes = serializeResponse(response)
        self.fileObject.write(responseBytes)
        self.fileObject.flush()
