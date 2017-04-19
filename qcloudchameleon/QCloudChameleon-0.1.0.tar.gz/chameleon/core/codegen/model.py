# coding: UTF-8

from property import *
import os


class OCModel:
    def __init__(self, name, secondName=None):
        self.name = name
        self.secondName = secondName
        self.properties = []
        self.comment = None

    def checkPropertyExist(self, p):
        for pItor in self.properties:
            if pItor.name == p.name:
                print("--------\n")
                print(pItor.name)
                return True
        return False

    def addProperty(self, p):
        assert(isinstance(p , Property))
        if self.checkPropertyExist(p):
            raise NameError("property has exist before, you input another [%s]" % (p.name))
        if (self.comment != None):
            p.comment = self.comment
            self.comment = None
            pass
        self.properties.append(p)

    def hasContainerClass(self):
        for p in self.properties:
            if isinstance(p, NSArrayProperty):
                return True
                pass
            pass
        pass
        return False
    def cacheComment(self, comment):
        self.comment = comment
        pass
