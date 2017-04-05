from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^leader_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<project>[A-Za-z]+)/log/$', test, name='leader_log'),
    url(r'^admin_user/(?P<username>[A-Z0-9][0-9]{7})/(?P<project>[A-Za-z]+)/log/$', test, name='admin_log'),
]
