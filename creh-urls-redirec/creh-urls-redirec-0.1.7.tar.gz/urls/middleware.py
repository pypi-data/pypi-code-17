from django.shortcuts import redirect
from actions import register


class UrlRedirectMiddleware():
    """
    This middleware lets you match a specific url and redirect the request to a
    new url.

    You keep a tuple of url regex pattern/url redirect tuples on your site
    settings, example:

    URL_REDIRECTS = (
        (r'www\.example\.com/hello/$', 'http://hello.example.com/'),
        (r'www\.example2\.com/$', 'http://www.example.com/example2/'),
    )

    """
    def process_request(self, request):
        host = request.META['PATH_INFO']
        redirect_url = register.update_count_views_url(host)
        if redirect_url == host:
            pass
        else:
            return redirect(redirect_url)