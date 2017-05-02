from abc import ABCMeta, abstractmethod

class NameExtractor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getCommandName(self, command):
        pass
