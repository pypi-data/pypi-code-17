from .nameextractor import NameExtractor

class ClassNameExtractor(NameExtractor):
    def getCommandName(self, command):
        return command.__class__.__name__
