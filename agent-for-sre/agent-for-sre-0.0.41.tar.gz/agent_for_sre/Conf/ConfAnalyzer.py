#!/usr/bin/python
# encoding: utf-8
import yaml
from .Conf import Conf

class ConfAnalyzer(Conf):
	__yaml_content={}
	__products=[]
	__f=''
	def __init__(self,yamlfile):
		try:
			self.__f = open(yamlfile)
		except:
			raise Exception("cannot open",yamlfile)
		else:
			self.__yaml_content = yaml.load(self.__f)

	def getProducts(self):
		self.__products=self.__yaml_content.keys()
		return(self.__products)

	def getEnnameByProduct(self,pname):
		return(self.__yaml_content[pname]['enname-list'])

	def getMonitorByProduct(self,pname):
		return(self.__yaml_content[pname]['monitor'])

	def getMonitorMonitorlistByProduct(self,pname):
		return(self.__yaml_content[pname]['monitor']['monitor_list'])

	def getMonitorDevicelistByProduct(self,pname):
		return(self.__yaml_content[pname]['monitor']['device_list'])

	def getDataByL4(self,l0,l1,l2,l3,l4):
		return(self.__yaml_content[l0][l1][l2][l3][l4])

	def getDataByL3(self,l0,l1,l2,l3):
		return(self.__yaml_content[l0][l1][l2][l3])

	def getDataByL2(self,l0,l1,l2):
		return(self.__yaml_content[l0][l1][l2])

	def getDataByL1(self,l0,l1):
		return(self.__yaml_content[l0][l1])

	def getDataByL0(self,l0):
		return(self.__yaml_content[l0])

	def __del__(self):
		try:
			self.__f.close()
		except:
			raise Exception("close error",self.__f)
