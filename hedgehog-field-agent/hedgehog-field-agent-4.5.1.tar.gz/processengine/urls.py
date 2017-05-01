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
from processengine.views import AllProcessViewSet, run_process_definition, HictoricalExecutionViewSet, \
    RunningExecutionViewSet, AllExecutionViewSet, TaskResultViewSet

router = DefaultRouter()
router.register(r'data/(?P<execution>.+)/raw', TaskResultViewSet)
router.register(r'definitions', AllProcessViewSet)
router.register(r'executions', AllExecutionViewSet)
router.register(r'executions/(?P<process>.+)/history', HictoricalExecutionViewSet, base_name='historic')
router.register(r'executions/(?P<process>.+)/running', RunningExecutionViewSet, base_name='running')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^definition/(?P<pk>[0-9]+)/run', run_process_definition, name='run_process_definition'),
    # url(r'executions', HictoricalExecutionViewSet.as_view(),
    #     name='historical_executions'),
    # url(r'executions/(?P<slug>[0-9]+)', HictoricalExecutionViewSet.as_view({'get', 'get_completed_executions'}), name='historical_executions')
    # url(r'executions/(?P<slug>[0-9]+)', HictoricalExecutionViewSet.as_view(), name='historical_executions')
]
