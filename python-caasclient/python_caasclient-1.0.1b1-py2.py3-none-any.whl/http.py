# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-06 23:10:19
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-08 09:41:08
import requests

class HTTPClient(object):
	def __init__(self,endpoint,**kwargs):
		self.endpoint = endpoint
		# Authentication self.auth_token = kwargs.get('auth_token')
		self.api_version = kwargs.get('api_version')
		self.connection_params = kwargs.get('connection_params')

	def session(self):
		return requests.Session

	def make_url(self,**kwargs):
		pass

	def get(self):
		return self.session.get()
		
	def post(self):
		return self.session.post()

	def put(self):
		return self.session.put()

	def patch(self):
		return self.session.patch()

	def delete(self):
		return self.session.delete()

# class HTTPSession(object):