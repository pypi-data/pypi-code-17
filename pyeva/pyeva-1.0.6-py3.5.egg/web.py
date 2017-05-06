import json
import datetime
import logging
import pprint
import functools

import tornado.web
from tornado.escape import json_decode
from tornado.web import HTTPError, decode_signed_value
from tornado.log import app_log, gen_log
from tornado import httputil

# Import eva module
from eva.exceptions import EvaError

from eva.utils.backend import load_auth_backend
backend_auth = load_auth_backend()

# 定制 JSON Encoder
# http://stackoverflow.com/questions/19734724/django-is-not-json-serializable-when-using-ugettext-lazy
# https://docs.djangoproject.com/en/1.8/topics/serialization/
from eva.utils.functional import Promise
from eva.utils.encoding import force_text
from eva.core.serializers.json import DjangoJSONEncoder


class APIRequestHandler(tornado.web.RequestHandler):

    def fail(self, error="fail", errors=None, status=400, **kwargs):
        self.set_status(status)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        d = {"error": error}
        if kwargs:
            d.update(kwargs)
        if errors:
            d["errors"] = errors
        self.write(json.dumps(d, cls=LazyJSONEncoder))

    def fail_404(self, error="fail", errors=None, **kwargs):
        return self.fail(error, errors, status=404, **kwargs)

    def success(self, **kwargs):
        d = kwargs
        # 增加默认值
        if not d:
            d["status"] = "success"

        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps(d, cls=LazyJSONEncoder))

    def get_body_json(self):
        try:
            return json_decode(self.request.body)
        except:
            return {}

    @property
    def db(self):
        return self.application.db_session()

    @property
    def es(self):
        '''ElasticSearch'''
        return self.application.es

    def on_finish(self):
        self.application.db_session.remove()

    def get_current_user(self):
        self.require_setting("secret_key", "secure key")
        secret = self.application.settings["secret_key"]
        auth = self.request.headers.get('Authorization')
        if auth:
            x = auth.split()
            if len(x) == 2:
                # idea: 可以根据不同的 x[0] 使用不同的验证机制
                if x[0] == 'OOC':
                    sid = decode_signed_value(secret, "Sid", x[1])
                    if not sid:
                        logging.warning("fake sid!")
                        # FIXME!
                        # raise HTTPError(403, reason="fake_sid")
                        return
                    sid = sid.decode()
                    s = self.db.query(backend_auth.models.Session).filter_by(sid=sid).first()
                    if s:
                        if s.is_valid():
                            s.user.last_active = datetime.datetime.utcnow()
                            s.refresh_expired()
                            return s.user
                        else:
                            # FIXME!
                            # raise HTTPError(403, reason="session_expired")
                            logging.warn('%s: session is expired',
                                         s.user.username)

    def write_error(self, status_code, **kwargs):
        """定制出错返回
        """

        # TODO: 处理 status_code
        d = {"status_code": status_code}
        reason = kwargs.get('reason')

        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, HTTPError) and exception.reason:
                reason = exception.reason  # HTTPError reason!
            if isinstance(exception, HTTPError) and exception.status_code:
                status_code = exception.status_code  # HTTPError status_code!
            d["exc_info"] = str(exception)

        if reason:
            self.set_status(status_code, reason)
            self.fail(error=reason)
        else:
            self.set_status(status_code)
            self.fail(error="exception", data=d)

    def log_exception(self, typ, value, tb):
        """Override to customize logging of uncaught exceptions.

        By default logs instances of `HTTPError` as warnings without
        stack traces (on the ``tornado.general`` logger), and all
        other exceptions as errors with stack traces (on the
        ``tornado.application`` logger).

        .. versionadded:: 3.1
        """
        if isinstance(value, HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = ([value.status_code, self._request_summary()] +
                        list(value.args))
                gen_log.warning(format, *args)
        elif isinstance(value, EvaError):
            logging.error(value)
        else:
            app_log.error("Uncaught exception %s\n%r", self._request_summary(),
                          self.request, exc_info=(typ, value, tb))

    def show_debug(self):
        print("\n-- request:")
        print(self.request)
        print("\n-- request headers:")
        pprint.pprint(self.request.headers)
        print("\n-- request body:")
        json_body = self.get_body_json()
        if json_body:
            pprint.pprint(json_body)
        else:
            print(self.request.body)
        # print("\n")


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403, reason="need_auth")
        return method(self, *args, **kwargs)

    return wrapper


def administrator(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403, reason="need_auth")
        if not self.current_user.is_superuser:
            raise HTTPError(403, reason="no_perms")
        return method(self, *args, **kwargs)
    return wrapper


class HTTPError(Exception):
    """An exception that will turn into an HTTP error response.

    Raising an `HTTPError` is a convenient alternative to calling
    `RequestHandler.send_error` since it automatically ends the
    current function.

    To customize the response sent with an `HTTPError`, override
    `RequestHandler.write_error`.

    :arg int status_code: HTTP status code.  Must be listed in
        `httplib.responses <http.client.responses>` unless the ``reason``
        keyword argument is given.
    :arg string log_message: Message to be written to the log for this error
        (will not be shown to the user unless the `Application` is in debug
        mode).  May contain ``%s``-style placeholders, which will be filled
        in with remaining positional parameters.
    :arg string reason: Keyword-only argument.  The HTTP "reason" phrase
        to pass in the status line along with ``status_code``.  Normally
        determined automatically from ``status_code``, but can be used
        to use a non-standard numeric code.
    """

    def __init__(self, status_code, log_message=None, *args, **kwargs):
        self.status_code = status_code
        self.log_message = log_message
        self.args = args
        self.reason = kwargs.get('reason', None)
        if log_message and not args:
            self.log_message = log_message.replace('%', '%%')

    def __str__(self):
        message = "HTTP %d: %s" % (
            self.status_code,
            self.reason or httputil.responses.get(self.status_code, 'Unknown'))
        if self.log_message:
            return message + " (" + (self.log_message % self.args) + ")"
        else:
            return message


class LazyJSONEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyJSONEncoder, self).default(obj)
