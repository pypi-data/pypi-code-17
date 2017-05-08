# -*- coding: latin-1 -*-

'''
Created on Apr 10, 2016

@author: richard
'''
import logging
import webapp2
from webapp2_extras import sessions
import json
import traceback


class BaseHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data = json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)

    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        response_data = {}
        self.handle(None, response_data)

    def put(self):
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data = json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)


class BaseHandlerSession(BaseHandler):

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def request_print_status(self, code, message):
        self.response.clear()
        self.response.set_status(code)
        self.response.out.write(json.dumps(message))

    def clear_cache(self):
        self.session['user'] = None


class BaseHandlerAuthorized(BaseHandlerSession):

    def handle(self, received_json_data, response_data=None):
        user = self.session.get('user')

        if user:
            self.handle_auth_user(user, received_json_data)
        else:
            self.request_print_status(401, 'NOT AUTHORIZED')


class ExceptionHandler(BaseHandlerSession):

    def handle_500(self, request, http_status, exception):
        logging.critical('ERROR 500: %s ', str(exception))
        traceback.print_exc()
        return self.redirect('/error_redirect')


class ErrorRedirectHandler(BaseHandlerSession):
    def get(self):
        self.clear_cache()
        self.redirect('/')


class WarmUp(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Warmup successful')


# class BaseHandler(webapp2.RequestHandler):
#
#     def dispatch(self):
#         self.response.headers['Content-Type'] = self.get_type_content()
#         received_json_data = None
#
#         ### HANDLING EMPTY JSON....
#         try:
#             received_json_data = json.loads(self.request.body)
#         except ValueError:
#             pass
#
#         response_data = {}
#         self.handle(received_json_data, response_data)
#
#     def get(self):
#         pass
#
#     def put(self):
#         pass
#
#     def post(self):
#         pass
#
#     @classmethod
#     def get_type_content(cls):
#         return 'application/json'
#
#
# class BaseHandlerSession(BaseHandler):
#
#     def dispatch(self):
#         self.session_store = sessions.get_store(request=self.request)
#         try:
#             webapp2.RequestHandler.dispatch(self)
#         finally:
#             self.session_store.save_sessions(self.response)
#
#         super(BaseHandlerSession, self).dispatch()
#
#     @webapp2.cached_property
#     def session(self):
#         return self.session_store.get_session()
#
#     def request_print_status(self, code, message):
#         self.response.clear()
#         self.response.set_status(code)
#         self.response.out.write(json.dumps(message))
#
#     def clear_cache(self):
#         self.session['user'] = None
#
#
# class BaseHandlerAuthorized(BaseHandlerSession):
#
#     def handle(self, received_json_data, _=None):
#         user = self.session.get('user')
#
#         if user:
#             self.handle_auth_user(user, received_json_data)
#         else:
#             self.request_print_status(401, 'NOT AUTHORIZED')
#
#     def handle_auth_user(self, user, received_json_data):
#         raise NotImplemented
#
#
# class ExceptionHandler(BaseHandlerSession):
#
#     def handle_500(self, _, __, exception):
#         logging.critical('ERROR 500: %s ', str(exception))
#         traceback.print_exc()
#         #TODO: make this flexiable
#         return self.redirect('/error_redirect')
#
#
# class ErrorRedirectHandler(BaseHandlerSession):
#     def get(self):
#         self.clear_cache()
#         # TODO: make this flexiable
#         self.redirect('/')
#
#
# class WarmUp(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('Warmup successful')
#
