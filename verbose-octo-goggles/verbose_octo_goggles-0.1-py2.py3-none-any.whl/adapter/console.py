from .empty import EmptyAdapter


class ConsoleAdapter(EmptyAdapter):
    def upsert(self, data):
        print data
