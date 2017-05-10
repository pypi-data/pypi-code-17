#!/usr/bin/python
# encoding: utf-8
import dns.resolver
from .Collector import Collector

class DnsCollector(Collector):
	domain=''
	__my_resolver=''
	def __init__(self,domain):
		self.domain=domain
		self.__my_resolver = dns.resolver.Resolver()
		self.__my_resolver.nameservers = ['114.114.114.114']

	def getARecordByDnsname(self):
		result_A=[]
		try:
			answers_A = self.__my_resolver.query(self.domain, 'A')
		except:
			#print("A记录解析 ERROR")
			next
		else:
			for rdataA in answers_A:
				result_A.append(str(rdataA.address))
		return(result_A)

	def getCnameRecordByDnsname(self):
		result_cname=[]
		try:
			answers_CNAME = self.__my_resolver.query(self.domain, 'CNAME')
		except:
			#print("CNAME记录解析 ERROR")
			next
		else:
			for rdataC in answers_CNAME:
				result_cname.append(str(rdataC.target))
		return(result_cname)

	def getTxtRecordByDnsname(self):
		result_TXT=[]
		try:
			answers_TXT = self.__my_resolver.query(self.domain, 'TXT')
		except:
			#print("TXT记录解析 ERROR")
			next
		else:
			for rdata in answers_TXT:
				for txt_string in rdata.strings:
					result_TXT.append(rdata.address)
		return(result_TXT)

	def getMxRecordByDnsname(self):
		result_MX=[]
		try:
			answers_MX = self.__my_resolver.query(self.domain, 'MX')
		except:
			#print("MX记录解析 ERROR")
			next
		else:
			for rdata in answers_MX:
				for mx_string in rdata.strings:
					result_MX.append(mx_string)
		return(result_MX)

	def getAllInfoByDnsname(self):
		result=[]
		result={self.domain : {'A' : self.getARecordByDnsname(), 'CNAME': self.getCnameRecordByDnsname(), 'MX': self.getMxRecordByDnsname(), 'TXT': self.getTxtRecordByDnsname()}}
		return(result)

