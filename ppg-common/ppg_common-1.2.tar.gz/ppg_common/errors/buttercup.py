from tornado.web import HTTPError


class ButterCupHTTPErrors:
    X_SESSION_NOT_PROVIDED = (100, 400, 'Parameter not provided')
    NOT_VALID_X_SESSION = (101, 401, 'Parameter is not valid')
    NOT_AUTHORIZED = (102, 401, 'Not authorized')
    NO_ACTIVE_SESSION = (103, 404, 'There is not active session')
    INVALID_JSON_FORMAT = (104, 400, "Invalid json format")
    USER_ID_NOT_PROVIDED = (105, 400, 'User id is not provided')
    NOT_VALID_USER_ID = (106, 400, 'User id is not valid')
    TYPE_NOT_VALID = (107, 400, 'Wanted session type is not valid ')
    USER_HAS_SESSION = (108, 409, 'User already has a active session')
    SESSION_ID_NOT_PROVIDED = (109, 400, 'Session id not provided')
    SERVICE_NOT_DELETABLE = (110, 404, 'Service session can not be deleted')
    error_map = {
        100: X_SESSION_NOT_PROVIDED,
        101: NOT_VALID_X_SESSION,
        102: NOT_AUTHORIZED,
        103: NO_ACTIVE_SESSION,
        104: INVALID_JSON_FORMAT,
        105: USER_ID_NOT_PROVIDED,
        106: NOT_VALID_USER_ID,
        107: TYPE_NOT_VALID,
        108: USER_HAS_SESSION,
        109: SESSION_ID_NOT_PROVIDED,
        110: SERVICE_NOT_DELETABLE,
    }


class ButterCupHTTPException(HTTPError):
    def __init__(self, code_type):
        super(ButterCupHTTPException, self).__init__(code_type[1],
                                                     code_type[2])
        self.custom_code = code_type[0]
