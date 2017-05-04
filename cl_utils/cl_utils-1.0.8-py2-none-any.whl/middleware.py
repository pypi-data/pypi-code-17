"""It is to be used together with localeurl"""
from django import http
from django.conf import settings
from django.contrib.flatpages.views import flatpage
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.exceptions import MiddlewareNotUsed
from django.http import Http404, HttpResponse
from django.utils import translation


class FallbackMiddleware(object):
    """
    This middleware will not only do the lookups for FlatPage (based on path &
    /language/path), but also for Redirect.
    """
    def __init__(self):
        self.redirects = 'django.contrib.redirects' in settings.INSTALLED_APPS
        self.flatpages = 'django.contrib.redirects' in settings.INSTALLED_APPS
        if not self.redirects and not self.flatpages:
            raise MiddlewareNotUsed()

    def process_response(self, request, response):
        if not isinstance(response, HttpResponse) or response.status_code != 404:
            return response

        if self.flatpages:
            r = self.try_flatpage(request, request.path_info)
            if r is not None:
                return r
            # try it with language appended
            r = self.try_flatpage(request, '/%s%s' % (translation.get_language(), request.path_info))
            if r is not None:
                return r
            # ignore the flatpage attempt
        if self.redirects:
            r = self.try_redirect(request, request.path_info)
            if r is not None:
                return r
            # try it with language appended
            r = self.try_redirect(request, '/%s%s' % (translation.get_language(), request.path_info))
            if r is not None:
                return r

        return response

    def try_flatpage(self, request, path):
        '''See also FlatpageFallbackMiddleware.process_response'''
        try:
            return flatpage(request, path)
        except Http404:
            return None
        except:
            if settings.DEBUG:
                raise
            return None

    def try_redirect(self, request, path):
        '''See also RedirectFallbackMiddleware.process_response'''
        site = Site.objects.get_current()
        try:
            r = Redirect.objects.get(site__id__exact=site.id, old_path=path)
        except Redirect.DoesNotExist:
            r = None
        if r is None and settings.APPEND_SLASH:
            # Try removing the trailing slash.
            try:
                r = Redirect.objects.get(site__id__exact=site.id,
                                         old_path=path[:path.rfind('/')]+path[path.rfind('/')+1:])
            except Redirect.DoesNotExist:
                pass
        if r is not None:
            if r.new_path == '':
                return http.HttpResponseGone()
            return http.HttpResponsePermanentRedirect(r.new_path)
        return None
