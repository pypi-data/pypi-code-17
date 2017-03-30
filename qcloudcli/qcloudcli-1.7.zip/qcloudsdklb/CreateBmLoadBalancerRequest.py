#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateBmLoadBalancerRequest(Request):

	def __init__(self):
		Request.__init__(self, 'lb', 'qcloudcliV1', 'CreateBmLoadBalancer', 'lb.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetId(self):
		return self.get_params().get('subnetId')

	def set_subnetId(self, subnetId):
		self.add_param('subnetId', subnetId)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_loadBalancerType(self):
		return self.get_params().get('loadBalancerType')

	def set_loadBalancerType(self, loadBalancerType):
		self.add_param('loadBalancerType', loadBalancerType)

	def get_goodsNum(self):
		return self.get_params().get('goodsNum')

	def set_goodsNum(self, goodsNum):
		self.add_param('goodsNum', goodsNum)

	def get_payMode(self):
		return self.get_params().get('payMode')

	def set_payMode(self, payMode):
		self.add_param('payMode', payMode)

	def get_exclusive(self):
		return self.get_params().get('exclusive')

	def set_exclusive(self, exclusive):
		self.add_param('exclusive', exclusive)

	def get_tgwSetType(self):
		return self.get_params().get('tgwSetType')

	def set_tgwSetType(self, tgwSetType):
		self.add_param('tgwSetType', tgwSetType)

