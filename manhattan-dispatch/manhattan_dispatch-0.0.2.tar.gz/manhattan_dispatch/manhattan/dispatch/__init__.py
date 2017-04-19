from flask import current_app, url_for
from werkzeug.wsgi import DispatcherMiddleware

__all__ = ['Dispatcher']


class Dispatcher:
    """
    Allows one to mount middlewares or applications in a WSGI application.

    This is useful if you want to combine multiple WSGI applications::

        app = DispatcherMiddleware(app, {
            '/app2':        app2,
            '/app3':        app3
        })

    """

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}
        self.url_for_resolver = URLForResolver(
            [self.app] + list(self.mounts.values())
            )

    def __call__(self, environ, start_response):
        script = environ.get('PATH_INFO', '')
        path_info = ''

        while '/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit('/', 1)
            path_info = '/%s%s' % (last_item, path_info)
        else:
            app = self.mounts.get(script, self.app)

        original_script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = original_script_name + script

        # Convert empty path info values to a forward slash '/'
        environ['PATH_INFO'] = path_info or '/'

        return app(environ, start_response)


class URLForResolver:
    """
    A URL resolver that provides resolution of `url_for` across multiple apps.
    """

    def __init__(self, apps):
        self.apps = apps
        self.cache = {}

        for app in apps:
            app.url_build_error_handlers.append(self)

    def __call__(self, error, endpoint, values):
        """Attempt to resolve a URL any of the registered apps"""

        # Check if we have a cached look up
        if endpoint in self.cache:
            app = self.cache[endpoint]
            if app:
                with app.app_context(), app.test_request_context():
                    return url_for(endpoint, **values)
            else:
                raise error

        # Attempt to find an app with the registered endpoint
        for app in self.apps:

            # No point in checking the current app
            if app is current_app:
                continue

            for rule in app.url_map.iter_rules():

                if rule.endpoint == endpoint:
                    # Found - cache the result and call self to return the URL
                    self.cache[endpoint] = app
                    return self(error, endpoint, values)

        # Not found - cache the result and re-raise the error
        self.cache[endpoint] = None
        raise error
