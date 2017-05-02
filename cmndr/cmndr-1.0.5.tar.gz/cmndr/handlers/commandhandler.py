from cmndr.middleware import Middleware
from .nameextractors import NameExtractor
from .inflectors import Inflector
from .locators import Locator

class CommandHandler(Middleware):
    _extractor = None
    _locator = None
    _inflector = None

    def __init__(self, extractor, locator, inflector):
        # type: (CommandExtractor, Locator, Inflector)
        self._extractor = extractor
        self._locator = locator
        self._inflector = inflector

    def execute(self, command, nextCallable):
        commandName = self._extractor.getCommandName(command)
        handler = self._locator.getHandlerForCommand(commandName)
        method = self._inflector.getMethod(command, handler)

        nextCallable(command)

        return getattr(handler, method)(command)
