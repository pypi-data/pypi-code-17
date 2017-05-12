from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^signup/$', views.signup, name = 'signup'),
	url(r'^login/$', views.login, name = 'login'),
	url(r'^logout/$', views.logout, name = 'logout'),
	url(r'^signup-and-get-token/$', views.signup_and_get_token, name = 'signup_and_get_token'),
	url(r'^login-and-get-token/$', views.login_and_get_token, name = 'login_and_get_token'),
]


