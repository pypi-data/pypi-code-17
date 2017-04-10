from django.conf.urls import url
from . import views
from .views import ReaGraph


urlpatterns = [
	#url(r'^$', views.file_list, name='list'),
    url(r'^regGraph/$', views.regGraph, name='regGraph'),
    url(r'^regGraphFile/(?P<system_id>\d+)/$', views.regGraphFile, name ='regGraphCreateFromFile'),
    url(r'^regGraphQuick/(?P<system_id>\d+)/$', views.regGraphQuick, name ='regGraphCreateFromQuick'),
    url(r'^reaGraph/$', views.reaGraph, name='reaGraph'),
    url(r'^reaGraph/(?P<system_id>\d+)/$', ReaGraph.as_view(), name='reaGraphCreate'),
    # url(r'^upload/(?P<slug>[\w-]+)/$', views.file_upload, name ='upload'),
    url(r'^delete/(?P<pk>\d+)/$', views.graph_delete, name="delete"),
    # url(r'^delete/(?P<slug>[\w-]+)/$', views.file_delete_project, name="delete_project"),
    # url(r'^load/(?P<id>\d+)/$', views.file_load, name="load"),

]