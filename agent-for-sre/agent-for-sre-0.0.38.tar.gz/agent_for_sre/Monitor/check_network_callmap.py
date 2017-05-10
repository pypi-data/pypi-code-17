#!/usr/bin/python
# encoding: utf-8
import yaml,re
import tarfile,datetime
import requests
import dns.resolver

def dns_resolve_check(ip,monitor_item):
	error=0
	for domain in monitor_item['dns_name']:
		my_resolver = dns.resolver.Resolver()
		my_resolver.nameservers = monitor_item['nameservers']
		
		if(monitor_item['dns_record_a']!=''):
			try:
				answers_A = my_resolver.query(domain, 'A')
			except:
				print(domain,monitor_item['dns_record_a'],"A记录解析 ERROR")
			else:
				for rdata in answers_A:
					if(str(rdata.address) in monitor_item['dns_record_a']):
						print(domain,rdata.address,'A记录 OK')
					else:
						error=1
						print(domain, rdata.address,'A记录 ERROR')
						print('A记录应该为:', domain, monitor_item['dns_record_a'])
			
		if(monitor_item['dns_record_cname']!=''):
			try:
				answers_CNAME = my_resolver.query(domain, 'CNAME')
			except:
				print(domain,monitor_item['dns_record_cname'],"CNAME记录解析ERROR")
			else:
				for rdata in answers_CNAME:
					if(str(rdata.target) == monitor_item['dns_record_cname']):
						print(domain, rdata.target,'cname记录 OK')
					else:
						error=1
						print(domain, rdata.target,'cname记录 ERROR')
						print('cname记录应该为:',domain, monitor_item['dns_record_cname'])
			
		if(monitor_item['dns_record_txt']!=''):
			try:
				answers_TXT = my_resolver.query(domain, 'TXT')
			except:
				print(domain,monitor_item['dns_record_txt'],"TXT记录解析 ERROR")
			else:
				for rdata in answers_TXT:
					for txt_string in rdata.strings:
						if(rdata.address==monitor_item['dns_record_txt']):
							print(domain, txt_string,'TXT记录 OK')
						else:
							error=1
							print(domain, txt_string,'TXT记录 ERROR')
							print('TXT记录应该为:',domain, monitor_item['dns_record_txt'])
	return(error)
		
def url_check(ip,monitor_item):
	error=0

	#设定参数
	import pycurl
	try:
	    from io import BytesIO
	except ImportError:
	    from StringIO import StringIO as BytesIO
	
	for protocal in monitor_item['protocal']:
		for host_bind in monitor_item['host_bind']:
			for port in monitor_item['port']:
				for uri in monitor_item['uri']:
					buffer = BytesIO();c = pycurl.Curl()
					url=str(protocal)+"://"+str(host_bind)+""+":"+str(port)+""+str(uri)
					c.setopt(c.URL, url);c.setopt(c.TIMEOUT, monitor_item['timeout']);c.setopt(c.WRITEDATA, buffer);c.setopt(c.RESOLVE, [host_bind+":"+str(port)+":"+ip])
				
					try:
						c.perform()
					except:
						error+=1
						print(ip,url,str(monitor_item['chname']),"network ERROR")
					else:
						if(str(monitor_item['return_content'])!=''):
							if(buffer.getvalue().decode('utf-8').replace('\n', '')==monitor_item['return_content']):
								print(ip,url,str(monitor_item['chname']),'OK')
							else:
								error+=1
								print(ip,url,str(monitor_item['chname']),buffer.getvalue().decode('utf-8').replace('\n', ''),monitor_item['return_content'],'ERROR')
						elif(str(monitor_item['return_code']!='')):
							if(str(c.getinfo(c.RESPONSE_CODE))==str(monitor_item['return_code'])):
								print(ip,url,str(monitor_item['chname']),'OK')
							else:
								error+=1
								print(ip,url,str(monitor_item['chname']),str(c.getinfo(c.RESPONSE_CODE)),str(monitor_item['return_code']),'ERROR')
						else:
							error+=1
							print(ip,url,str(monitor_item['chname']),'ERROR')
	return(error)

def check_network_callmap(algo_data):
	error_num=0
	i=''
	for i in algo_data['device_list']:
		print("------------------------------------------")
		print("第",i['step'],"步",i['name'])
		for ip in i['ips']:
			for k in i['monitor_items']:
				error_num+=eval(algo_data['monitor_list'][k]['function']+"(ip,algo_data['monitor_list'][k])")
	return(error_num)

if __name__ == '__main__':
	# 处理命令行参数
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--product", choices=['cia','gzq','x3','oss','ccp','www.chanjet.com','exam','tplusexam','service.chanjet.com','t.chanjet.com'],required=True, help="输入产品名称")
	args = parser.parse_args()

	# 开始进行主流程，打开配置文件开始执行
	yamlfile=args.product+"/"+args.product+".yaml"
	f = open(yamlfile)
	x = yaml.load(f)
	error_num=0
	for i in x[0]['algo_list']:
		print("------------------------------------------")
		print("run "+i['name'])
		error_num+=eval(i['name']+"(i)")
	exit(error_num)

