# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^DjangoProject/~create/$",
        view=views.DjangoProjectCreateView.as_view(),
        name='DjangoProject_create',
    ),
    url(
        regex="^DjangoProject/(?P<pk>\d+)/~delete/$",
        view=views.DjangoProjectDeleteView.as_view(),
        name='DjangoProject_delete',
    ),
    url(
        regex="^DjangoProject/(?P<pk>\d+)/$",
        view=views.DjangoProjectDetailView.as_view(),
        name='DjangoProject_detail',
    ),
    url(
        regex="^DjangoProject/(?P<pk>\d+)/~update/$",
        view=views.DjangoProjectUpdateView.as_view(),
        name='DjangoProject_update',
    ),
    url(
        regex="^DjangoProject/$",
        view=views.DjangoProjectListView.as_view(),
        name='DjangoProject_list',
    ),
	url(
        regex="^ProductionConfDjangoProject/~create/$",
        view=views.ProductionConfDjangoProjectCreateView.as_view(),
        name='ProductionConfDjangoProject_create',
    ),
    url(
        regex="^ProductionConfDjangoProject/(?P<pk>\d+)/~delete/$",
        view=views.ProductionConfDjangoProjectDeleteView.as_view(),
        name='ProductionConfDjangoProject_delete',
    ),
    url(
        regex="^ProductionConfDjangoProject/(?P<pk>\d+)/$",
        view=views.ProductionConfDjangoProjectDetailView.as_view(),
        name='ProductionConfDjangoProject_detail',
    ),
    url(
        regex="^ProductionConfDjangoProject/(?P<pk>\d+)/~update/$",
        view=views.ProductionConfDjangoProjectUpdateView.as_view(),
        name='ProductionConfDjangoProject_update',
    ),
    url(
        regex="^ProductionConfDjangoProject/$",
        view=views.ProductionConfDjangoProjectListView.as_view(),
        name='ProductionConfDjangoProject_list',
    ),
	]
