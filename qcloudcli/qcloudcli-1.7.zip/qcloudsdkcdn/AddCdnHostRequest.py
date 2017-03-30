#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class AddCdnHostRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdn', 'qcloudcliV1', 'AddCdnHost', 'cdn.api.qcloud.com')

	def get_origin(self):
		return self.get_params().get('origin')

	def set_origin(self, origin):
		self.add_param('origin', origin)

	def get_host(self):
		return self.get_params().get('host')

	def set_host(self, host):
		self.add_param('host', host)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_hostType(self):
		return self.get_params().get('hostType')

	def set_hostType(self, hostType):
		self.add_param('hostType', hostType)

