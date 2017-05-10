#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class WafCollector(Collector):
	__wafip=''
	def __init__(self,wafip):
		self.__wafip=wafip

	def getUpstreamByWafip(self):
			next
	
	def GetAllInstanceIp():
		# Instances数据格式 {'i-25c6vsn1k': u'172.16.101.7'....}
		Instances = {}
		InstancesPageCount = GetPageCount(100,GetInstancesConf)
		for i in range(1,InstancesPageCount+1):
			Instances_val = GetInstancesConf(i,100)
			Instances_dic = json.loads(Instances_val)
			for Instance in Instances_dic['Instances']['Instance']:
				InstanceId = str(Instance['InstanceId'])
				IpAddress_list = Instance['VpcAttributes']['PrivateIpAddress']['IpAddress']
				if len(IpAddress_list)>0:
					Instances[InstanceId] = IpAddress_list[0]
				else:
					Instances[InstanceId] = ''
		return Instances
	
	def GetEipAddressesRequest(PageNumber=None,PageSize=None):
		EipAddresses = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
		EipAddresses.set_accept_format('json')
		if PageNumber != None:
			EipAddresses.set_PageNumber(PageNumber)
		if PageSize != None:
			EipAddresses.set_PageSize(PageSize)
		EipAddresses_val = clt.do_action(EipAddresses)
		#print EipAddresses_val
		return EipAddresses_val
	
	def GetAliEipData():
		Eips = {}
		insert_data = []
		now_time = GetNowTime()
		idc = 'ali'
		Instances = GetAllInstanceIp()
		EipsPageCount = GetPageCount(50,GetEipAddressesRequest)
		for i in range(1,EipsPageCount+1):
			print i
			EipAddresses_val = GetEipAddressesRequest(i,50)
			EipAddresses_dic = json.loads(EipAddresses_val)
			for EipAddress in EipAddresses_dic['EipAddresses']['EipAddress']:
				Eip = str(EipAddress['IpAddress'])
				InstanceId = EipAddress['InstanceId']
				if InstanceId=='':
					ipaddress = ' '
				else:
					ipaddress = Instances[InstanceId]
				row_data = [Eip,ipaddress,InstanceId,str(now_time),idc]
				insert_data.append(row_data)
		return insert_data
	
	def GetVpcEipData():
		insert_data=[]
		idc = 'ali'
		NetworkType='vpc'
		now_time = GetNowTime()
		LoadBalancers_val = GetLoadBalancers(NetworkType)
		LoadBalancers_dic = json.loads(LoadBalancers_val)
		#print LoadBalancers_dic
		LoadBalancers = LoadBalancers_dic['LoadBalancers']['LoadBalancer']
		for LoadBalancer in LoadBalancers:
			LoadBalancerId = LoadBalancer['LoadBalancerId']
			Eip = LoadBalancer['Address']
			ipaddress=Eip
			InstanceId=LoadBalancer['VpcId']
			row_data = [Eip,ipaddress,InstanceId,str(now_time),idc]
			insert_data.append(row_data)
		#print insert_data
		return insert_data
	
	def getAllIpByWafip(self):
		self.getUpstreamByWafip()
