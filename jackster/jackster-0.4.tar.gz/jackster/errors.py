from jackster.funcs import status, chain
from jackster.funcs.templates import render

import os
from traceback import extract_tb

def errorMessage(newStatus, description):
    return [status(newStatus), render('error.html', status=newStatus, description=description)]

def error500(req, res, nxt, exception):
    chain(status(500), render(
        'error_500.html',
        show_traceback=(os.getenv('DEBUG', '').lower() == 'true'),
        exception=exception,
        traceback=extract_tb(exception.__traceback__)
    ))(req, res, nxt)

defaultErrors = {
    400: errorMessage(400, 'Bad request.'),
    401: errorMessage(401, 'Unauthorized.'),
    402: errorMessage(402, 'Payment Required.'),
    403: errorMessage(403, 'Forbidden.'),
    404: errorMessage(404, 'Not Found.'),
    405: errorMessage(405, 'Method Not Allowed.'),
    406: errorMessage(406, 'Not Acceptable.'),
    407: errorMessage(407, 'Proxy Authentication Required.'),
    408: errorMessage(408, 'Request Time-out.'),
    409: errorMessage(409, 'Conflict.'),
    410: errorMessage(410, 'Gone.'),
    411: errorMessage(411, 'Length Required.'),
    412: errorMessage(412, 'Precondition failed.'),
    413: errorMessage(413, 'Payload Too Large.'),
    414: errorMessage(414, 'URI Too Long.'),
    415: errorMessage(415, 'Unsupported Media Type.'),
    416: errorMessage(416, 'Range Not Satisfiable.'),
    417: errorMessage(417, 'Expectation Failed.'),
    418: errorMessage(418, 'I\'m a teapot.'),
    421: errorMessage(421, 'Misdirected Request.'),
    422: errorMessage(422, 'Unprocessable Entity.'),
    423: errorMessage(423, 'Locked.'),
    424: errorMessage(424, 'Failed Dependency.'),
    426: errorMessage(426, 'Upgrade Required.'),
    428: errorMessage(428, 'Precondition Required.'),
    429: errorMessage(429, 'Too Many Requests.'),
    431: errorMessage(431, 'Request Header Fields Too Large.'),
    451: errorMessage(451, 'Unavailable For Legal Reasons.'),
    500: error500,
    501: errorMessage(501, 'Not Implemented.'),
    502: errorMessage(502, 'Bad Gateway.'),
    503: errorMessage(503, 'Service Unavailable.'),
    504: errorMessage(504, 'Gateway Time-out.'),
    505: errorMessage(505, 'HTTP Version Not Supported.'),
    506: errorMessage(506, 'Variant Also Negotiates.'),
    507: errorMessage(507, 'Insufficient Storage.'),
    508: errorMessage(508, 'Loop Detected.'),
    510: errorMessage(510, 'Not Extended.'),
    511: errorMessage(511, 'Network Authentication Required.'),
}
