from .inflector import Inflector

class CallableInflector(Inflector):
    def getMethod(self, command, commandHandler):
        return '__call__'
