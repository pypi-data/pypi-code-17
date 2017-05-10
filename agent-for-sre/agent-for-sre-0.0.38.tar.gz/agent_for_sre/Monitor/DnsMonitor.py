#!/usr/bin/python
# encoding: utf-8
import dns.resolver
from .Monitor import Monitor

class DnsMonitor(Monitor):
	def dns_resolve_check(self):
		self.result=[]
		if(self.monitor_item['function']!='dns_resolve_check'):
			self.result.append({'ip':self.ip,'msg':"not dns_resolve_check function",'error':101})
			return(self.result)
		for domain in self.monitor_item['dns_name']:
			my_resolver = dns.resolver.Resolver()
			my_resolver.nameservers = self.monitor_item['nameservers']
			
			if(self.monitor_item['dns_record_a']!=''):
				try:
					answers_A = my_resolver.query(domain, 'A')
				except:
					self.result.append({'domain':domain,'item':self.monitor_item['dns_record_a'],'msg':"A记录解析 ERROR",'error':1})
					#print(domain,self.monitor_item['dns_record_a'],"A记录解析 ERROR")
				else:
					for rdata in answers_A:
						if(str(rdata.address) in self.monitor_item['dns_record_a']):
							self.result.append({'domain':domain,'item':rdata.address,'msg':'A记录 OK','error':0})
							#print(domain,rdata.address,'A记录 OK')
						else:
							self.result.append({'domain':domain,'item':rdata.address,'msg':'A记录 ERROR','error':1})
							#print(domain, rdata.address,'A记录 ERROR')
							self.result.append({'domain':domain,'item':self.monitor_item['dns_record_a'],'msg':'A记录应该为','error':1})
							#print('A记录应该为:', domain, self.monitor_item['dns_record_a'])
				
			if(self.monitor_item['dns_record_cname']!=''):
				try:
					answers_CNAME = my_resolver.query(domain, 'CNAME')
				except:
					self.result.append({'domain':domain,'item':self.monitor_item['dns_record_cname'],'msg':'CNAME记录解析ERROR','error':1})
					#print(domain,self.monitor_item['dns_record_cname'],"CNAME记录解析ERROR")
				else:
					for rdata in answers_CNAME:
						if(str(rdata.target) == self.monitor_item['dns_record_cname']):
							self.result.append({'domain':domain,'item':rdata.target,'msg':'cname记录 OK','error':0})
							#print(domain, rdata.target,'cname记录 OK')
						else:
							self.result.append({'domain':domain,'item':rdata.target,'msg':'cname记录 ERROR','error':1})
							#print(domain, rdata.target,'cname记录 ERROR')
							self.result.append({'domain':domain,'item':self.monitor_item['dns_record_cname'],'msg':'cname记录应该为','error':1})
							#print('cname记录应该为:',domain, self.monitor_item['dns_record_cname'])
				
			if(self.monitor_item['dns_record_txt']!=''):
				try:
					answers_TXT = my_resolver.query(domain, 'TXT')
				except:
					self.result.append({'domain':domain,'item':self.monitor_item['dns_record_txt'],'msg':'TXT记录解析 ERROR','error':1})
					#print(domain,self.monitor_item['dns_record_txt'],"TXT记录解析 ERROR")
				else:
					for rdata in answers_TXT:
						for txt_string in rdata.strings:
							if(txt_string==self.monitor_item['dns_record_txt']):
								self.result.append({'domain':domain,'item':txt_string,'msg':'TXT记录OK','error':0})
								#print(domain, txt_string,'TXT记录 OK')
							else:
								self.result.append({'domain':domain,'item':txt_string,'msg':'TXT记录ERROR','error':1})
								#print(domain, txt_string,'TXT记录 ERROR')
								self.result.append({'domain':domain,'item':self.monitor_item['dns_record_txt'],'msg':'TXT记录应该为','error':1})
								#print('TXT记录应该为:',domain, self.monitor_item['dns_record_txt'])
		return(self.result)
