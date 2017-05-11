#!/usr/bin/python
# encoding: utf-8
import psutil
from .ProcessCollector import ProcessCollector

class NetinfoProcessCollector(ProcessCollector):
	def __init__(self,pinfo):
		self.__state_pids=list()
		self.__state_net_listen_list=[]
		self.__state_net_est_list=[]
		#super(NetinfoProcessCollector,self).__init__(pinfo)
		self.pinfo=pinfo

	def __get_net_listen_list_by_pid(self,mode):
		self.__state_pids=ProcessCollector.getPids(self)
		for pid in self.__state_pids:
			p=psutil.Process(pid)
			for i in p.connections():
				i=list(i)
				if(i[5]=="LISTEN"):
					if(mode=='simple'):
						self.__state_net_listen_list.append(i[3])
					else:
						self.__state_net_listen_list.append(i)

	def __get_net_est_list_by_pid(self,mode):
		self.__state_pids=ProcessCollector.getPids(self)
		for pid in self.__state_pids:
			p=psutil.Process(pid)
			for i in p.connections():
				i=list(i)
				if(i[5]=="ESTABLISHED"):
					if(mode=='simple'):
						self.__state_net_est_list.append(i[3])
					else:
						self.__state_net_est_list.append(i)

	def get_net_listen_list(self,mode=''):
		self.__get_net_listen_list_by_pid(mode)
		return(self.__state_net_listen_list)
	def get_net_est_list(self,mode=''):
		self.__get_net_est_list_by_pid(mode)
		return(self.__state_net_est_list)
