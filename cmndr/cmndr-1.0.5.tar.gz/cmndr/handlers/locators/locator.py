from abc import ABCMeta, abstractmethod

class Locator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getHandlerForCommand(self, command):
        pass
