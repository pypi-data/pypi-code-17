#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector
from nsnitro import *

class NetscalerCollector(Collector):
	__nsip=''
	__user=''
	__password=''
	def __init__(self,nsip,user,password):
		self.__nsip=nsip
		self.__user=user
		self.__password=password

	def getUpstreamByNsip(self):
		nitro = NSNitro(self.__nsip,self.__user,self.__password)
		nitro.login()
		insert_data = []
		for lb in NSLBVServer.get_all(nitro):
				lb_type = 'ns'
				lb_name = lb.get_name()
				lb_ip = lb.get_ipv46()
				lb_status = lb.get_status()
				lb_port = lb.get_port()
				lb_protocol = lb.get_servicetype()
				#print lb.get_name() + " " + lb.get_ipv46() + " "
				#print lb.get_port()
				#print lb.get_status()
				name = lb.get_name()
				info = {}
				lbbinding = NSLBVServerServiceGroupBinding()
				lbbinding.set_name(name)
				lbbindings = NSLBVServerServiceGroupBinding.get(nitro, lbbinding)
				for lbb in lbbindings:
					sgn = lbb.get_servicegroupname()
					for i in NSServiceGroupServerBinding.get(nitro,lbb):
						#print i.get_ip()
						#print i.get_port()
						bk_ip = str(i.get_ip())
						bk_port = str(i.get_port())
						info[bk_ip]= bk_port

				lbservice = NSLBVServerServiceBinding()
				lbservice.set_name(name)
				lbservices = NSLBVServerServiceBinding.get(nitro,lbservice)
				for service in lbservices:
					#print service
					sn = service.get_servicename()
					#print sn
					sbk_ip=str(service.get_ipv46())
					sbk_port=str(service.get_port())
					info[sbk_ip]=sbk_port

				bk_info = json.dumps(info)
				row_data = [lb_type,lb_name,lb_ip,lb_port,lb_protocol,lb_status,bk_info]
				insert_data.append(row_data)

	def getAllInfoByNsip(self):
		self.getUpstreamByNsip()
