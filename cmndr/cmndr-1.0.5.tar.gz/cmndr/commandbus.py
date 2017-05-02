from cmndr.middleware import Middleware
from cmndr.handlers.middlewarehandler import MiddlewareHandler
from cmndr.exception.invalidmiddlewareexception import InvalidMiddlewareException

class CommandBus:
    def __init__(self, middleware):
        # type: (List)
        self._middleware = self._create_execution_chain(middleware)

    def handle(self, command):
        return self._middleware(command)

    def _create_execution_chain(self, middlewareList):
        # type: (List)
        handler = lambda command: None

        while True:
            try:
                middleware = middlewareList.pop()
                if (not isinstance(middleware, Middleware)):
                    raise InvalidMiddlewareException('{0} is not an instance of Middleware'.format(middleware.__class__.__name__))
                handler = MiddlewareHandler(middleware, handler)
            except IndexError:
                return handler

        return lastMiddleware
