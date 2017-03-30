#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateCdbHourRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cdb', 'qcloudcliV1', 'CreateCdbHour', 'cdb.api.qcloud.com')

	def get_engineVersion(self):
		return self.get_params().get('engineVersion')

	def set_engineVersion(self, engineVersion):
		self.add_param('engineVersion', engineVersion)

	def get_cdbType(self):
		return self.get_params().get('cdbType')

	def set_cdbType(self, cdbType):
		self.add_param('cdbType', cdbType)

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

	def get_goodsNum(self):
		return self.get_params().get('goodsNum')

	def set_goodsNum(self, goodsNum):
		self.add_param('goodsNum', goodsNum)

	def get_memory(self):
		return self.get_params().get('memory')

	def set_memory(self, memory):
		self.add_param('memory', memory)

	def get_volume(self):
		return self.get_params().get('volume')

	def set_volume(self, volume):
		self.add_param('volume', volume)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_cdbInstanceId(self):
		return self.get_params().get('cdbInstanceId')

	def set_cdbInstanceId(self, cdbInstanceId):
		self.add_param('cdbInstanceId', cdbInstanceId)

	def get_instanceRole(self):
		return self.get_params().get('instanceRole')

	def set_instanceRole(self, instanceRole):
		self.add_param('instanceRole', instanceRole)

