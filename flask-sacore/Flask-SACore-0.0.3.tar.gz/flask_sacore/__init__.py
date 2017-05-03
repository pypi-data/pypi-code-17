# from flask import current_app
from sqlalchemy import create_engine

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class SAConnection(object):

    def __init__(self, connection, transaction):
        self.connection = connection
        self.transaction = transaction


class SACore(object):

    def __init__(self, dsn, app=None):
        self.app = app
        self.dsn = dsn
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.engine = create_engine(self.dsn)
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        connection = self.engine.connect()
        transaction = connection.begin()
        return SAConnection(connection, transaction)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'sacore_db'):
            for dsn, connection in ctx.sacore_db.items():
                transaction = connection.transaction
                if transaction.is_active:
                    if exception is not None:
                        transaction.rollback()
                    else:
                        transaction.commit()
                ctx.sacore_db[dsn].connection.close()

    @property
    def con(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sacore_db'):
                ctx.sacore_db = {}
            if self.dsn not in ctx.sacore_db:
                ctx.sacore_db[self.dsn] = self.connect()
            return ctx.sacore_db[self.dsn].connection
