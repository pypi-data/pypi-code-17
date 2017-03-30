#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateProductRequest(Request):

	def __init__(self):
		Request.__init__(self, 'iiot', 'qcloudcliV1', 'CreateProduct', 'iiot.api.qcloud.com')

	def get_productProperties(self):
		return self.get_params().get('productProperties')

	def set_productProperties(self, productProperties):
		self.add_param('productProperties', productProperties)

	def get_defaultPolicyName(self):
		return self.get_params().get('defaultPolicyName')

	def set_defaultPolicyName(self, defaultPolicyName):
		self.add_param('defaultPolicyName', defaultPolicyName)

	def get_productName(self):
		return self.get_params().get('productName')

	def set_productName(self, productName):
		self.add_param('productName', productName)

