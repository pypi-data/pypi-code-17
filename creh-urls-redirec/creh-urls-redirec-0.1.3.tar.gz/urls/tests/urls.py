from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^url_source2/$', views.empty, name='url_source2'),
]