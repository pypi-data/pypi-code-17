class PubSubSupport:
    """
    Use as mixin. Example:
    PubSubSupport().on('event', lambda event: ...)
    """

    def __init_subclass__(self):
        self.__listeners = []

    def on(self, etype, handler):
        self.__listeners += [(etype, handler)]
        return self

    def fire(self, event):
        return list(handler(event) for etype, handler
                    in self.__listeners if isinstance(event, etype))

    class Event:
        def __init__(self, name):
            self.name = name
