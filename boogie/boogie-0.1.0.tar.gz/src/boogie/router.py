'''
Url routing and views
=====================

Regex-based routing is flexible, powerful, is a pain to debug and certainly is
not hip. Of course we can do crazy stuff with our urls, but most of the time
they pretend to work as a filesystem.

Django-boogie url router does translates nice url template expressions to those
low-level regexes that Django understands.

.. code-block:: python

    from boogie.router import route


    @route('user/{user:username}/')
    def user_detail(user: User):
        """
        Prints user detail.
        """
        return '<p>Hello %s!</p>' % user.get_full_name()

'''
import inspect
from functools import wraps


class Router:
    """

    """

    @property
    def urls(self):
        """
        Urls converted to a Django-friendly format.
        """
        return []

    def __init__(self, routes):
        self.routes = list(routes)

    def __call__(self, url, **kwargs):
        def decorator(func):
            self.register(func, url, **kwargs)
            return func

        return decorator

    def register(self, func, url,
                 perms=None, login_required=None, login_page=None,
                 content_type=None):
        pass


class Route:
    def __init__(self, data):
        self.data = data

    def regex(self):
        """
        Return the equivalent regex for the route.
        """


def wrap_request(func, request_param='request'):
    """
    Inspect if func receives a 'request' as first param and returns a function
    that accepts this parameter.

    Args:
        func:
            The wrapping function.
        request_param:
            A string with the expected name for the request param.
    """

    # Check if function already has the correct signature
    args = inspect.getargspec(func).args
    if args and args[0] == request_param:
        return func

    # Function receives request, but not as a first argument
    if request_param in inspect.signature(func).parameters:
        @wraps(func)
        def wrapped(*args, **kwargs):
            request, *args = args
            return func(*args, request=request, **kwargs)

        wrapped.function = getattr(func, 'function', func)
        return wrapped

    # Function does not receive a request parameter at all
    @wraps(func)
    def wrapped(*args, **kwargs):
        request, *args = args
        return func(*args, **kwargs)

    wrapped.function = getattr(func, 'function', func)
    return wrapped
