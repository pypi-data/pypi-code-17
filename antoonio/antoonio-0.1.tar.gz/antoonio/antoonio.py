import os
import hashlib
import hmac
import base64

def hash(data, key):
    hashed = hmac.new(key, msg=data, digestmod=hashlib.sha256).digest()
    return base64.b16encode(hashed).decode().lower()

def printSep(char = "=", widthModifier = 0.6):
    width = int(int(os.popen("stty size", "r").read().split()[1]) * widthModifier)
    print (char * ((width/1)+1))[:width]