#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class EcsMachineCollector(Collector):
	__ecsip=''
	def __init__(self,ecsip):
		self.__wafip=ecsip

	def getLocationByWafip(self):
		next

	def getAllInfoByEcsip(self):
		self.getLocationByWafip()
