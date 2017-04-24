"""orchestrator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from rest_framework.routers import DefaultRouter

from assetadapter import views
from assetadapter.views import AssetViewSet, PropertyViewSet, ActiveDeviceListView, InactiveDeviceListView

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'devicemanager/active', ActiveDeviceListView)
router.register(r'devicemanager/inactive', InactiveDeviceListView)
# router.register(r'devicemanager/unknown', UnknownDeviceListView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^unit/(?P<pk>[0-9]+)/choices', views.list_unit_choices, name='unit_choices'),
    url(r'^property/(?P<pk>[0-9]+)/choices', views.list_property_value_choices, name='unit_choices'),
    url(r'^devicemanager/attach$', views.devicemanager_attach, name='devicemanager_attach'),
    # url(r'^devicemanager/unknown$', views.devicemanager_attach, name='devicemanager_unknown'),
]
