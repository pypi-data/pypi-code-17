#!/usr/bin/python
# encoding: utf-8
class Monitor:
	ip=''
	monitor_item={}
	result=[]

	def __init__(self,ip,monitor_item):
		self.ip=ip
		self.monitor_item=monitor_item
