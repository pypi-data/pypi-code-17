class RequestError(Exception):
    def __init__(self, status, message):
        super(RequestError, self).__init__(message)
        self.status = status
        self.message = message
