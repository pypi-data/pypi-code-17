from tornado.web import HTTPError


class PpgHTTPError(HTTPError):
    def __init__(self, code_type):
        # Call the base class constructor with the parameters it needs
        """
        :param code_type is from BlossomHTTPErrors
        """
        super(PpgHTTPError, self).__init__(code_type[1], code_type[2])
        self.custom_code = code_type[0]


class PpgHttpErrors(object):
    WENT_WRONG = (99, 500, "Something went wrong")
    error_map = {
        99: WENT_WRONG
    }
