
from .ORGDocument import * 

class ORGFile(object):
    
    def __init__(self, path):
        self.path = path 
        f = open(path)
        self.document = ORGDocument.parse(f.read().split("\n"))
        f.close()

    def getDocument(self):
        return self.document
