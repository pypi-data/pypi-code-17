import exception

def intToBytes(n):
    b = bytearray([0, 0, 0, 0])   # init
    b[0] = n & 0xFF
    b[1] = (n >> 8) & 0xFF
    b[2] = (n >> 16) & 0xFF
    b[3] = (n >> 24) & 0xFF
    return b

def bytesToInt(b):
    n = (b[0] & 0xFF) | ((b[1] & 0xFF) << 8) | ((b[2] & 0xFF) << 16) | ((b[3] & 0xFF) << 24)
    return n


def readNBytes(fileObject, n):
    readBytes = bytearray(fileObject.read(n))

    if len(readBytes) != n:
        raise exception.FuncioException("Bytes read do not equal exepected bytes")

    return readBytes