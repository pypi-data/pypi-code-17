from abc import ABCMeta, abstractmethod

class Middleware:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, command, nextCallable):
        pass
