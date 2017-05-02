from .locator import Locator

class InMemoryLocator(Locator):
    def __init__(self, handlers):
        self._mappings = {}
        self.addHandlers(handlers)

    def addHandler(self, handler, commandClass):
        self._mappings[commandClass] = handler

    def addHandlers(self, handlers):
        for handler in handlers:
            self.addHandler(handler, handlers.get(handler))

    def getHandlerForCommand(self, commandName):
        return self._mappings[commandName]
