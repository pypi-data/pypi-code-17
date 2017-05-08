from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^visited-products/$', views.visited_products, name='visited-products'),
]
