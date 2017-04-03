"""
Easy construction of a tree of multiple Klein() apps

This makes it convenient to construct a system of classes like the following,
where each class handles a portion of the route tree.

class TheFirst(object):
    app = klein.Klein()

    @app.route('/api/', branch=True)
    @enter('mymod.TheSecond')
    def apiTree(self, request, subKlein):
        # Do any setup here that is shared by routes under /api/
        return subKlein

class TheSecond(object):
    app = klein.Klein()

    @app.route('/anything')
    def anything(self, request):
        ....


In the above system, a request for GET '/api/anything' will be handled by
TheSecond.anything()
"""
import functools

from twisted.python.reflect import namedAny


def enter(clsQname):
    """
    Delegate a rule to another class which instantiates a Klein app

    This also memoizes the resource instance on the handler function itself
    """
    def wrapper(routeHandler):
        @functools.wraps(routeHandler)
        def inner(self, request, *a, **kw):
            if getattr(inner, '_subKlein', None) is None:
                cls = namedAny(clsQname)
                inner._subKlein = cls().app.resource()
            return routeHandler(self, request, inner._subKlein, *a, **kw)
        inner._subKleinQname = clsQname
        return inner
    return wrapper


