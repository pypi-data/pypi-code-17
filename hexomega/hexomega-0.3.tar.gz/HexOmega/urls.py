"""HexOmega URL Configuration

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
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import javascript_catalog

from ajax_select import urls as ajax_select_urls

import users.urls
import log.urls
import users.other

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'admin/jsi18n/', javascript_catalog),
    url(r'', include(users.urls)),
    url(r'ajax_select/', include(ajax_select_urls)),
    # url(r'^log/', include(log.urls)),
    url(r'^overlord/', users.other.overlord),
]
