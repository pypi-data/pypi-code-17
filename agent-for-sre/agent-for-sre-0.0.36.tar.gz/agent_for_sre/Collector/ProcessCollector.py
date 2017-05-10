#!/usr/bin/python
# encoding: utf-8
import psutil
from .Collector import Collector

class ProcessCollector(Collector):
	def __init__(self,pinfo):
		self.pinfo=pinfo

	def getPids(self):
		pname=self.pinfo['pname']
		pids=[]
		for proc in psutil.process_iter():
			pinfo = proc.as_dict(attrs=['pid', 'name','cmdline'])
			if (pname in str(pinfo['cmdline'])):
				if ('grep' not in str(pinfo['cmdline'])):
					pids.append(pinfo['pid'])
		return(pids)

	def getPinfo(self):
		print(self.pinfo)
