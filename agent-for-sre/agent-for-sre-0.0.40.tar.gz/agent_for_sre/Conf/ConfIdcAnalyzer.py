#!/usr/bin/python
# encoding: utf-8
import yaml
from .Conf import Conf

class ConfIdcAnalyzer(Conf):
	__yaml_content={}
	__types=[]
	__f=''
	def __init__(self,yamlfile):
		try:
			self.__f = open(yamlfile)
		except:
			raise Exception("cannot open",yamlfile)
		else:
			self.__yaml_content = yaml.load(self.__f)

	def getTypes(self):
		self.__types=self.__yaml_content.keys()
		return(self.__types)

	def getNetrangeByName(self,idcname):
		return(self.__yaml_content['net']['net-range-list'][idcname])

