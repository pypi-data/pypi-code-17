#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join, dirname
from flask_login import LoginManager

from flask import Blueprint, current_app, send_from_directory, redirect, request, send_file
from .controllers.login_controller import login, logout, add_user, get_user, set_user
from .util import Unauthorized
from .models.users import Users

def static_web_index():
    return send_from_directory(join(dirname(__file__),'swagger-ui'),"index.html")

def static_web(filename):
    if filename == "index.html":
        return redirect(request.url[:-1 * len('index.html')])
    if filename == "swagger.yaml":
        swagger = open(join(dirname(__file__),'swagger-ui','swagger.yaml'),'r').read()
        swagger = swagger.replace('$host$', "%s:%s" % (request.environ['SERVER_NAME'], request.environ['SERVER_PORT']) )
        swagger = swagger.replace('$path$', [current_app.blueprints[i] for i in current_app.blueprints if current_app.blueprints[i].__class__.__name__ == 'BlueLogin'][0].url_prefix )
        return swagger
    return send_from_directory(join(dirname(__file__),'swagger-ui'),filename)

class BlueLogin(Blueprint):

    def __init__(self, name='bluelogin', import_name=__name__, ui_testing=False, *args, **kwargs):
        Blueprint.__init__(self, name, import_name, *args, **kwargs)
        self._users = {}
        self._add_url_rule(ui_testing)
        self.before_app_first_request(self._init_login_manager)
    
    def _init_login_manager(self):
        self._login_manager = LoginManager()
        self._login_manager.init_app(current_app)
        current_app.secret_key = 'super secret string'

        @self._login_manager.user_loader
        def load_user(id):
            return Users().get_user(id)
        
        current_app.logger.debug("add login manager")
    
    def _add_url_rule(self, ui_testing=False):
        self.add_url_rule('/logout', 'logout', logout, methods=['GET'])
        self.add_url_rule('/login', 'login', login, methods=['PUT'])
        self.add_url_rule('/user', 'add_user', add_user, methods=['PUT'])
        self.add_url_rule('/user/<userId>', 'get_user', get_user, methods=['GET'])
        self.add_url_rule('/user/<userId>', 'set_user', set_user, methods=['PUT'])
        if ui_testing:
            self.add_url_rule('/login/ui/<path:filename>', 'static_web', static_web)
            self.add_url_rule('/login/ui/', 'static_web_index', static_web_index)
    

