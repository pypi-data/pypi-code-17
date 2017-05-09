# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-07 22:29:31
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-08 10:02:29


class Manager(object):
	
	def __init__(self,api):
		self.api = api

	def make_path(self, id):
		return '/' + api.api_version + '/' + \
			self.api_name + '/%s' % id if id else \
			'/' + api.api_version + '/' + self.api_name

	def list(self):
		pass

	def get(self, id):
		pass

	def create(self, id):
		pass

	def filter(self, id):
		pass
		
	def delete(self, id):
		api.delete(make_path(id))


	
