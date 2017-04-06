#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class UpdateCdnConfigRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'UpdateCdnConfig', 'cdn.api.qcloud.com')

	def get_hostId(self):
		return self.get_params().get('hostId')

	def set_hostId(self, hostId):
		self.add_param('hostId', hostId)

	def get_cache(self):
		return self.get_params().get('cache')

	def set_cache(self, cache):
		self.add_param('cache', cache)

	def get_cacheMode(self):
		return self.get_params().get('cacheMode')

	def set_cacheMode(self, cacheMode):
		self.add_param('cacheMode', cacheMode)

	def get_refer(self):
		return self.get_params().get('refer')

	def set_refer(self, refer):
		self.add_param('refer', refer)

	def get_fwdHost(self):
		return self.get_params().get('fwdHost')

	def set_fwdHost(self, fwdHost):
		self.add_param('fwdHost', fwdHost)

	def get_fullUrl(self):
		return self.get_params().get('fullUrl')

	def set_fullUrl(self, fullUrl):
		self.add_param('fullUrl', fullUrl)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_origin(self):
		return self.get_params().get('origin')

	def set_origin(self, origin):
		self.add_param('origin', origin)

	def get_middleResource(self):
		return self.get_params().get('middleResource')

	def set_middleResource(self, middleResource):
		self.add_param('middleResource', middleResource)

