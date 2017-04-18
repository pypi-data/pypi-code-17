"""visaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'visa', views.UserViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'assets', views.AssetViewSet)



urlpatterns = [
    # url(r'^$', views.health, name='health'),

    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # url(r'^$', TemplateView.as_view(template_name= 'index.html'), name='home'),
    # url(r'^$', 'django.contrib.staticfiles.views.serve', kwargs={'path': 'index.html', 'document_root': '/static/'}),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^devicemanager/attach$', views.devicemanager_attach, name='devicemanager_attach'),
    url(r'^devicemanager/active', views.devicemanager_active, name='devicemanager_active'),
    url(r'^devicemanager/inactive$', views.devicemanager_inactive, name='devicemanager_inactive'),
    url(r'^devicemanager/unknown$', views.devicemanager_unknown, name='devicemanager_unknown'),
    url(r'^visa/list$', views.visa_list, name='visa_list'),
    url(r'^visa/alias', views.visa_alias, name='visa_alias'),
    url(r'^visa/read$', views.visa_read, name='visa_read'),
    url(r'^visa/write', views.visa_write, name='visa_write'),
    url(r'^visa/query', views.visa_query, name='visa_query'),

    # ex: /polls/5/
    url(r'^(?P<asset_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<asset_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]