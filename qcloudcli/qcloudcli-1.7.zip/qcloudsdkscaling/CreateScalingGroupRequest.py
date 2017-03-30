#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateScalingGroupRequest(Request):

	def __init__(self):
		Request.__init__(self, 'scaling', 'qcloudcliV1', 'CreateScalingGroup', 'scaling.api.qcloud.com')

	def get_scalingGroupName(self):
		return self.get_params().get('scalingGroupName')

	def set_scalingGroupName(self, scalingGroupName):
		self.add_param('scalingGroupName', scalingGroupName)

	def get_scalingConfigurationId(self):
		return self.get_params().get('scalingConfigurationId')

	def set_scalingConfigurationId(self, scalingConfigurationId):
		self.add_param('scalingConfigurationId', scalingConfigurationId)

	def get_minSize(self):
		return self.get_params().get('minSize')

	def set_minSize(self, minSize):
		self.add_param('minSize', minSize)

	def get_maxSize(self):
		return self.get_params().get('maxSize')

	def set_maxSize(self, maxSize):
		self.add_param('maxSize', maxSize)

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_subnetIds(self):
		return self.get_params().get('subnetIds')

	def set_subnetIds(self, subnetIds):
		self.add_param('subnetIds', subnetIds)

	def get_removePolicy(self):
		return self.get_params().get('removePolicy')

	def set_removePolicy(self, removePolicy):
		self.add_param('removePolicy', removePolicy)

	def get_loadBalancerIds(self):
		return self.get_params().get('loadBalancerIds')

	def set_loadBalancerIds(self, loadBalancerIds):
		self.add_param('loadBalancerIds', loadBalancerIds)

	def get_zoneIds(self):
		return self.get_params().get('zoneIds')

	def set_zoneIds(self, zoneIds):
		self.add_param('zoneIds', zoneIds)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_desiredCapacity(self):
		return self.get_params().get('desiredCapacity')

	def set_desiredCapacity(self, desiredCapacity):
		self.add_param('desiredCapacity', desiredCapacity)

	def get_healthyCheckType(self):
		return self.get_params().get('healthyCheckType')

	def set_healthyCheckType(self, healthyCheckType):
		self.add_param('healthyCheckType', healthyCheckType)

