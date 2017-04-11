from django.conf.urls import url
from .views import DefaultWebsocketView


urlpatterns = [
    url(r'(?P<event>[\w\-_]+)', DefaultWebsocketView.as_view())
]
