from ppg_common.errors import (
    BubblesHttpError,
    ButterCupHTTPException,
    BlossomHTTPError,
    PpgHTTPError
)
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-session')
        self.set_header('Access-Control-Allow-Methods',
                        'GET,PUT,PATCH,POST,DELETE,OPTIONS')

    def options(self):
        self.set_status(204)

    def write_error(self, status_code, **kwargs):
        exc_class, exc_obj, traceback = kwargs.get('exc_info')
        if any([exc_class is err for err in [
            BubblesHttpError,
            BlossomHTTPError,
            ButterCupHTTPException,
            PpgHTTPError
        ]]):
            self.finish({
                'message': exc_obj.log_message,
                'code': exc_obj.custom_code
            })
        else:
            self.finish({
                'message': traceback,
                'code': 'unknown'
            })
