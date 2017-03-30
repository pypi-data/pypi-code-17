#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyCdbCharsetRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdb', 'qcloudcliV1', 'ModifyCdbCharset', 'cdb.api.qcloud.com')

	def get_cdbInstanceId(self):
		return self.get_params().get('cdbInstanceId')

	def set_cdbInstanceId(self, cdbInstanceId):
		self.add_param('cdbInstanceId', cdbInstanceId)

	def get_charset(self):
		return self.get_params().get('charset')

	def set_charset(self, charset):
		self.add_param('charset', charset)

