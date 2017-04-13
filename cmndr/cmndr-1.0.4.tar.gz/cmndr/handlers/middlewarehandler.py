class MiddlewareHandler:
    def __init__(self, middleware, nextCallable):
        self._middleware = middleware
        self._nextCallable = nextCallable

    def __call__(self, command):
        ret = self._middleware.execute(command, self._nextCallable)
        return ret
