#!/usr/bin/python
# encoding: utf-8
import psutil,re
from .ProcessCollector import ProcessCollector

class FileinfoProcessCollector(ProcessCollector):
	__logfile_list=[]
	__file_list=[]

	def __init__(self,pinfo):
		super(FileinfoProcessCollector,self).__init__(pinfo)

	def __get_logfile_opened_list_by_pid(self):
		self.__state_pids=ProcessCollector.getPids(self)
		for pid in self.__state_pids:
			p=psutil.Process(pid)
			print(p.cmdline())
			for i in p.open_files():
				i=list(i)
				if(re.search('var/log',i[0])):
					self.__logfile_list.append(i[0])

	def __get_file_opened_list_by_pid(self):
		self.__state_pids=ProcessCollector.getPids(self)
		for pid in self.__state_pids:
			p=psutil.Process(pid)
			print(p.cmdline())
			for i in p.open_files():
				i=list(i)
				self.__file_list.append(i[0])
		
	def get_logfile_list(self):
		self.__get_logfile_opened_list_by_pid()
		print(self.__logfile_list)
	def get_file_list(self):
		self.__get_file_opened_list_by_pid()
		print(self.__file_list)
