#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class PhysicalMachineCollector(Collector):
	__ip=''
	def __init__(self,ip):
		self.__ip=ip

	def getUpstreamByIp(self):
		next

	def getAllInfoByIp(self):
		self.getUpstreamByIp()
