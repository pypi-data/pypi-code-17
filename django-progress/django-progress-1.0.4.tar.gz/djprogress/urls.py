from django.conf.urls import patterns, url, include

urlpatterns = patterns('djprogress.views',
    url(r'^$', 'overview', name='djprogress_overview'),
    url(r'^exception/(?P<progress_id>\d+)/$', 'show_exception', name='djprogress_show_exception'),
    url(r'^resolve/(?P<progress_id>\d+)/$', 'resolve', name='djprogress_resolve'),
    url(r'^api/get/$', 'api_get_progress', name='djprogress_api_get'),
)
