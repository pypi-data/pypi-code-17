from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<otp_key>\w+)/$', views.otl_view, name='one-time-link'),
]
