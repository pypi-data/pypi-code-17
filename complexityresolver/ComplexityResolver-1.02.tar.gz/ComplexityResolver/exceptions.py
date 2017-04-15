class ArgumentException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(NotImplementedException, self).__init__(message)


class NotImplementedException(Exception):
    pass


class TimeoutException(Exception):
    pass
