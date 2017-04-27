LEVEL_ERROR = 1
LEVEL_INFO = 2
LEVEL_WARNING = 3

LEVEL_CHOICES = (
    (LEVEL_ERROR, 'Error'),
    (LEVEL_INFO, 'Info'),
    (LEVEL_WARNING, 'Warning')
)

STATUS_ACTIVE = 1
STATUS_ARCHIVED = 2
STATUS_DELETED = 3

STATUS_CHOICES = (
    (STATUS_ACTIVE, 'Active'),
    (STATUS_ARCHIVED, 'Archived'),
    (STATUS_DELETED, 'Deleted')
)


CODE_400 = 'Bad Request'
CODE_401 = 'Unauthorized'
CODE_403 = 'Forbidden'
CODE_404 = 'Not Found'
CODE_405 = 'Method Not Allowed'
CODE_406 = 'Not Acceptable'
CODE_407 = 'Proxy Authentication Required'
CODE_408 = 'Request Timeout'
CODE_409 = 'Conflict'
CODE_410 = 'Gone'
CODE_411 = 'Length Required'
CODE_412 = 'Precondition Failed'
CODE_413 = 'Request Entity Too Large'
CODE_414 = 'Request-URI Too Long'
CODE_415 = 'Unsupported Media Type'
CODE_416 = 'Requested Range Not Satisfiable'
CODE_417 = 'Expectation Failed'
CODE_418 = 'I am a teapot'
CODE_422 = 'Unprocessable Entity (WebDAV - RFC 4918)'
CODE_423 = 'Locked (WebDAV - RFC 4918)'
CODE_424 = 'Failed Dependency (WebDAV) (RFC 4918)'
CODE_425 = 'Unassigned'
CODE_426 = 'Upgrade Required (RFC 7231)'
CODE_428 = 'Precondition Required'
CODE_429 = 'Too Many Requests'
CODE_431 = 'Request Header Fileds Too Large)'
CODE_449 = 'Argument not optional'
CODE_451 = 'Unavailable for Legal Reasons'

CODE_CHOICES = (
    ('400', CODE_400),
    ('401', CODE_401),
    ('403', CODE_403),
    ('404', CODE_404),
    ('405', CODE_405),
    ('406', CODE_406),
    ('407', CODE_407),
    ('408', CODE_408),
    ('409', CODE_409),
    ('410', CODE_410),
    ('411', CODE_411),
    ('412', CODE_412),
    ('413', CODE_413),
    ('414', CODE_414),
    ('415', CODE_415),
    ('416', CODE_416),
    ('417', CODE_417),
    ('418', CODE_418),
    ('422', CODE_422),
    ('423', CODE_423),
    ('424', CODE_424),
    ('425', CODE_425),
    ('426', CODE_426),
    ('428', CODE_428),
    ('429', CODE_429),
    ('431', CODE_431),
    ('449', CODE_449),
    ('451', CODE_451),
)