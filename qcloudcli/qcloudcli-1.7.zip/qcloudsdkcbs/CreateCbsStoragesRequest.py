#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class CreateCbsStoragesRequest(Request):

	def __init__(self):
		Request.__init__(self, 'cbs', 'qcloudcliV1', 'CreateCbsStorages', 'cbs.api.qcloud.com')

	def get_storageSize(self):
		return self.get_params().get('storageSize')

	def set_storageSize(self, storageSize):
		self.add_param('storageSize', storageSize)

	def get_goodsNum(self):
		return self.get_params().get('goodsNum')

	def set_goodsNum(self, goodsNum):
		self.add_param('goodsNum', goodsNum)

	def get_period(self):
		return self.get_params().get('period')

	def set_period(self, period):
		self.add_param('period', period)

	def get_zoneId(self):
		return self.get_params().get('zoneId')

	def set_zoneId(self, zoneId):
		self.add_param('zoneId', zoneId)

	def get_storageType(self):
		return self.get_params().get('storageType')

	def set_storageType(self, storageType):
		self.add_param('storageType', storageType)

	def get_projectId(self):
		return self.get_params().get('projectId')

	def set_projectId(self, projectId):
		self.add_param('projectId', projectId)

	def get_snapshotId(self):
		return self.get_params().get('snapshotId')

	def set_snapshotId(self, snapshotId):
		self.add_param('snapshotId', snapshotId)

