#!/usr/bin/python
# encoding: utf-8
import pycurl,re
from .Monitor import Monitor

class UrlMonitor(Monitor):
	def url_check(self):
		self.result=[]
		try:
		    from io import BytesIO
		except ImportError:
		    from StringIO import StringIO as BytesIO
		
		for protocal in self.monitor_item['protocal']:
			for host_bind in self.monitor_item['host_bind']:
				for port in self.monitor_item['port']:
					for uri in self.monitor_item['uri']:
						buffer = BytesIO();c = pycurl.Curl()
						url=str(protocal)+"://"+str(host_bind)+""+":"+str(port)+""+str(uri)
						c.setopt(c.URL, url);c.setopt(c.TIMEOUT, self.monitor_item['timeout']);c.setopt(c.WRITEDATA, buffer);c.setopt(c.RESOLVE, [host_bind+":"+str(port)+":"+self.ip])
					
						try:
							c.perform()
						except:
							self.result.append({'ip':self.ip,'url':url,'msg':"network ERROR",'error':1})
							#print(self.ip,url,str(self.monitor_item['chname']),"network ERROR")
						else:
							if(str(self.monitor_item['return_content'])!=''):
								if(self.monitor_item['return_content'] in re.compile(r'(\r|\n|\s|\t)').sub("",buffer.getvalue().decode('utf-8'))):
									self.result.append({'ip':self.ip,'url':url,'msg':str(self.monitor_item['chname'])+' OK','error':0})
									#print(self.ip,url,str(self.monitor_item['chname']),'OK')
								else:
									self.result.append({'ip':self.ip,'url':url,'msg':str(self.monitor_item['chname'])+re.compile(r'(\r|\n|\s|\t)').sub("",buffer.getvalue().decode('utf-8'))+self.monitor_item['return_content']+'ERROR','error':1})
									#print(self.ip,url,str(self.monitor_item['chname']),buffer.getvalue().decode('utf-8').replace('\n', ''),self.monitor_item['return_content'],'ERROR')
							elif(str(self.monitor_item['return_code']!='')):
								if(str(c.getinfo(c.RESPONSE_CODE))==str(self.monitor_item['return_code'])):
									self.result.append({'ip':self.ip,'url':url,'msg':str(self.monitor_item['chname'])+' OK','error':0})
									#print(self.ip,url,str(self.monitor_item['chname']),'OK')
								else:
									self.result.append({'ip':self.ip,'url':url,'msg':str(self.monitor_item['chname'])+str(c.getinfo(c.RESPONSE_CODE))+str(self.monitor_item['return_code'])+'ERROR','error':1})
									#print(self.ip,url,str(self.monitor_item['chname']),str(c.getinfo(c.RESPONSE_CODE)),str(self.monitor_item['return_code']),'ERROR')
							else:
								self.result.append({'ip':self.ip,'url':url,'msg':str(self.monitor_item['chname']),'error':1})
								#print(self.ip,url,str(self.monitor_item['chname']),'ERROR')
			return(self.result)
