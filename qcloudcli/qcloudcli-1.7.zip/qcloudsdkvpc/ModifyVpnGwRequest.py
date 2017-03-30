#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class ModifyVpnGwRequest(Request):

	def __init__(self):
		Request.__init__(self, 'vpc', 'qcloudcliV1', 'ModifyVpnGw', 'vpc.api.qcloud.com')

	def get_vpcId(self):
		return self.get_params().get('vpcId')

	def set_vpcId(self, vpcId):
		self.add_param('vpcId', vpcId)

	def get_vpnGwId(self):
		return self.get_params().get('vpnGwId')

	def set_vpnGwId(self, vpnGwId):
		self.add_param('vpnGwId', vpnGwId)

	def get_vpnGwName(self):
		return self.get_params().get('vpnGwName')

	def set_vpnGwName(self, vpnGwName):
		self.add_param('vpnGwName', vpnGwName)

	def get_isAutoRenewals(self):
		return self.get_params().get('isAutoRenewals')

	def set_isAutoRenewals(self, isAutoRenewals):
		self.add_param('isAutoRenewals', isAutoRenewals)

	def get_localSlaIp(self):
		return self.get_params().get('localSlaIp')

	def set_localSlaIp(self, localSlaIp):
		self.add_param('localSlaIp', localSlaIp)

	def get_sslVpnPort(self):
		return self.get_params().get('sslVpnPort')

	def set_sslVpnPort(self, sslVpnPort):
		self.add_param('sslVpnPort', sslVpnPort)

