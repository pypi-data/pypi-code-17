from django.http import HttpResponsePermanentRedirect
from urls.actions import register

class UrlRedirectMiddleware:
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
        host = request.META['HTTP_HOST'] + request.META['PATH_INFO']
        redirect_url = register.update_count_views_url(host)

        return HttpResponsePermanentRedirect(redirect_url)