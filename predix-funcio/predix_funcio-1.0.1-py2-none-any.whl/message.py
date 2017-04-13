class Message(object):
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.headers == other.headers and self.body == other.body

    def __ne__(self, other):
        return not __eq__(self, other)

class Response(object):
    def __init__(self, statusCode, status, message):
        self.statusCode = statusCode
        self.status = status
        self.message = message

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.statusCode == other.statusCode and \
               self.status == other.status and \
               self.message == other.message

