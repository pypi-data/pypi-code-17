# coding: utf-8

from tornado.web import url

from . import views

handlers = [
    url(r'/auth/signup/identifier', views.SignUpIdentifier),
    url(r'/auth/signup', views.SignUp),
    url(r'/auth/signin', views.SignIn),
    url(r'/auth/signout', views.SignOut),
    url(r'/auth/forget_password/identifier', views.ForgetPasswordIdentifier),
    url(r'/auth/forget_password', views.ForgetPassword)
]
