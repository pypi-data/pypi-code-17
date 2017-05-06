# coding: utf-8

from tornado.web import url

from .console import views as console_views
from .admin import views as admin_views


handlers = [

    # console
    url(r'/console/account/profile', console_views.MyProfile),
    url(r'/console/account/password', console_views.PasswordReset),

    # console
    url(r'/admin/account/user', admin_views.UserHandler),
    url(r'/admin/account/user/([0-9]+)', admin_views.SingleUserHandler),
    url(r'/admin/account/user/([0-9]+)/profile', admin_views.SingleUserProfileHandler),
    url(r'/admin/account/user/([0-9]+)/password', admin_views.SingleUserPasswordHandler),

]
