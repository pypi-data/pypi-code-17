from django.conf.urls import url
from grafico_db import views

urlpatterns = [
    url(r'^$', views.mostrar_grafico),
]