from .inmemorylocator import InMemoryLocator

class LazyLoadingInMemoryLocator(InMemoryLocator):
    instances = {}

    def getHandlerForCommand(self, commandName):
        if commandName not in self.instances:
            self.instances[commandName] = super(LazyLoadingInMemoryLocator, self).getHandlerForCommand(commandName)()

        return self.instances[commandName]
