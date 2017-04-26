from contextlib import contextmanager
from flask import jsonify

from . import decorators
from . import errors
from . import reqparse

__version__ = '0.0.1'
__author__ = 'TuuZed'


class Toolbox(object):
    def __init__(self, app=None):
        self.app = app
        if app:
            self._register_error_handler()

    def init_app(self, app):
        self.app = app
        self._register_error_handler()

    def _register_error_handler(self):
        @self.app.errorhandler(errors.InvalidUsage)
        def handle_invalid_usage(error):
            resp = jsonify(error.to_dict())
            resp.status_code = error.status_code
            return resp

    @contextmanager
    def db_session(self, db):
        """
        取得数据库会话对象
        :param db: SQLAlchemy 对象
        :return:
        """
        session = db.session
        yield session
        session.close()
