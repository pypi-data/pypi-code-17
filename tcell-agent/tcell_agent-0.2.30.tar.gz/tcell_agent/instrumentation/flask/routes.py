import logging

from flask import Flask

from tcell_agent.agent import TCellAgent
from tcell_agent.instrumentation import safe_wrap_function

LOGGER = logging.getLogger('tcell_agent').getChild(__name__)


def calculate_route_id(method, uri):
    return str(hash('{method}|{uri}'.format(method=method.lower(), uri=uri)))


def get_methods(options, view_func):
    route_methods = options.get('methods', None)
    if route_methods is None:
        route_methods = getattr(view_func, 'methods', None) or ('get',)
    return [item.upper() for item in route_methods]


def discover_route(rule, view_func, options):
    for method in get_methods(options, view_func):
        try:
            # view_func can be a `functools.partial`. in that case, get
            # the wrapped function and report its information to tcell
            view_func = getattr(view_func, 'func', view_func)
            TCellAgent.discover_route(
                route_url=rule,
                route_method=method,
                route_target='.'.join([
                    getattr(view_func, '__module__', ''),
                    getattr(view_func, '__name__', ''),
                ]).strip('.') or "(dynamic)",
                route_id=calculate_route_id(method, rule)
            )
        except Exception as e:
            LOGGER.debug("Could not obtain route information: {e}".format(e=e))
            LOGGER.debug(e, exc_info=True)


def instrument_routes():
    old_flask_add_url_rule = Flask.add_url_rule

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        safe_wrap_function("Discover Flask Route", discover_route, rule, view_func, options)
        return old_flask_add_url_rule(self, rule, endpoint, view_func, **options)

    Flask.add_url_rule = add_url_rule
