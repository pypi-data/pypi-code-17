#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class MachineStatusCollectoer(Collector):
	__net_range=''

	def __init__(self,net_range):
		self.__net_range = net_range

	def getUpMachinesByConf(self):
		import nmap
		nm=nmap.PortScanner()
		nm.scan(hosts = " ".join(self.__net_range), arguments='-sn -PE -PS22,10622,3389 -n --min-hostgroup 1024 --min-parallelism 1024')
		hosts_up = [ x for x in nm.all_hosts()]
		return(hosts_up)

	def getUpMachinesByIpOrRange(self,ips):
		import nmap
		nm=nmap.PortScanner()
		nm.scan(hosts = ips, arguments='-sn -PE -PS22,10622,3389 -n --min-hostgroup 1024 --min-parallelism 1024')
		hosts_up = [ x for x in nm.all_hosts()]
		return(hosts_up)
