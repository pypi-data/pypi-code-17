"""rxncon_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from . import views
#from posts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^files/', include("fileTree.urls", namespace='fileTree')),
    url(r'^quick/', include("quick_format.urls", namespace='quick_format')),
    url(r'^graphs/', include("graphs.urls", namespace='graphs')),
    url(r'^bool/', include("boolean_model.urls", namespace='bool')),
    url(r'^rule_based/', include("rule_based.urls", namespace='rule_based')),
    url(r'^$', views.rxncon_site_index, name='index'),
    url(r'^publications$', views.publications, name='publications'),
    url(r'^funding', views.funding, name='funding'),
    url(r'^support', views.support, name='support'),
    url(r'^guided_tour', views.guided_tour, name='guided_tour'),
    #url(r'^delete/(?P<id>\d+)/$', fviews.file_delete, name="delete"),
    # url(r'^$', TemplateView.as_view(template_name='static_pages/index.html'),
    #     name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)