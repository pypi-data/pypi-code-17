#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class NginxCollector(Collector):
	__vip=''
	def __init__(self,vip):
		self.__vip=vip

	def getUpstreamByVip(self):
		next

	def getAllInfoByWip(self):
		self.getUpstreamByVip()
