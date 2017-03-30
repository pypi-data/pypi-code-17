#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DeleteNetworkAclRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'DeleteNetworkAcl', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_networkAclId(self):
		return self.get_params().get('networkAclId')

	def set_networkAclId(self, networkAclId):
		self.add_param('networkAclId', networkAclId)

