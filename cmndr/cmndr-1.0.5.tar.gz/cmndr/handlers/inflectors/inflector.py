from abc import ABCMeta, abstractmethod

class Inflector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getMethod(self, command, commandHandler):
        pass
