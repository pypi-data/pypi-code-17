# coding: utf-8

from tornado.web import url

from . import views

handlers = [
    url(r'/zen', views.Zen, name='zen:random'),
]
