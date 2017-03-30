#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class DescribeRedisRequest(Request):

	def __init__(self):
		Request.__init__(self, 'redis', 'qcloudcliV1', 'DescribeRedis', 'redis.api.qcloud.com')

	def get_redisId(self):
		return self.get_params().get('redisId')

	def set_redisId(self, redisId):
		self.add_param('redisId', redisId)

	def get_redisName(self):
		return self.get_params().get('redisName')

	def set_redisName(self, redisName):
		self.add_param('redisName', redisName)

	def get_limit(self):
		return self.get_params().get('limit')

	def set_limit(self, limit):
		self.add_param('limit', limit)

	def get_offset(self):
		return self.get_params().get('offset')

	def set_offset(self, offset):
		self.add_param('offset', offset)

	def get_orderBy(self):
		return self.get_params().get('orderBy')

	def set_orderBy(self, orderBy):
		self.add_param('orderBy', orderBy)

	def get_orderType(self):
		return self.get_params().get('orderType')

	def set_orderType(self, orderType):
		self.add_param('orderType', orderType)

	def get_projectIds(self):
		return self.get_params().get('projectIds')

	def set_projectIds(self, projectIds):
		self.add_param('projectIds', projectIds)

