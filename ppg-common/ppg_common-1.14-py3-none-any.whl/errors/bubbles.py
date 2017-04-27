from tornado.web import HTTPError


class BubblesHttpErrors(object):
    FORBIDDEN = (
        300, 403, 'Subject can not modify permissions over the object'
    )
    UNAUTHORIZED = (301, 401, 'Subject is not authorized')
    NOT_FOUND = (302, 404, 'Subject have no permissions')
    BAD_REQUEST = (303, 422, 'Bad parameters in request')
    INVALID_JSON = (304, 400, 'Invalid json format')
    NO_PERMISSIONS = (305, 404, 'No permissions for subject on object')
    MISSING_KEYS = (306, 422, 'Missing or too many keys')
    NOT_OWNER = (307, 403, 'Subject is not owner of the object')
    FALSE_PERMISSIONS = (308, 422, 'Can not set all false permissions')
    METHOD_NOT_ALLOWED = (309, 405, 'Method not allowed')
    UUID = (310, 400, 'UUID not valid')
    ROLLBACK = (311, 400, 'Session rolled back')
    DUPLICATED = (312, 409, 'Conflict occurred')

    error_map = {
        300: FORBIDDEN,
        301: UNAUTHORIZED,
        302: NOT_FOUND,
        303: BAD_REQUEST,
        304: INVALID_JSON,
        305: NO_PERMISSIONS,
        306: MISSING_KEYS,
        307: NOT_OWNER,
        308: FALSE_PERMISSIONS,
        309: METHOD_NOT_ALLOWED,
        310: UUID
    }


class BubblesHttpError(HTTPError):
    def __init__(self, code_type):
        super(BubblesHttpError, self).__init__(code_type[1], code_type[2])
        self.custom_code = code_type[0]
