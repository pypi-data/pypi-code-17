#!/usr/bin/python3
# encoding: utf-8
import psutil,sys,datetime,re
from agent_for_sre.Collector.NetinfoProcessCollector import NetinfoProcessCollector
from agent_for_sre.Collector.FileinfoProcessCollector import FileinfoProcessCollector
from agent_for_sre.Conf.ConfAnalyzer import ConfAnalyzer
from agent_for_sre.Monitor.DnsMonitor import DnsMonitor
from agent_for_sre.Monitor.UrlMonitor import UrlMonitor

def run(product):
	print()
	print("------------------------------------------")
	print("产品：",product)

	monitor_list=config.getMonitorMonitorlistByProduct(product)
	device_list=config.getMonitorDevicelistByProduct(product)

	count=0;new=[]
	for i in device_list:
		if(i['step']==count):
			new.append(i)
		count+=1
	device_list=new

	for device in device_list:
		print("------------------------------------------")
		print("第",device['step'],"步",device['name'])
		print("------------------------------------------")
		for ip in device['ips']:
			for item in device['monitor_items']:
				if(monitor_list[item]['function']=='url_check'):
					checker1=UrlMonitor(ip,monitor_list[item])
					for data1 in checker1.url_check():
						print(data1['ip'],data1['url'],data1['msg'])
				if(monitor_list[item]['function']=='dns_resolve_check'):
					checker2=DnsMonitor(ip,monitor_list[item])
					for data2 in checker2.dns_resolve_check():
						print(data2['domain'],data2['item'],data2['msg'])

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", required=True, help="输入yaml文件")
	parser.add_argument("-p", "--product", required=False, help="输入产品名")
	args = parser.parse_args()
	yamlfile=args.file

	config=ConfAnalyzer(yamlfile)

	product_list=[]
	if(args.product):
		product_list.append(args.product)
	else:
		product_list=config.getProducts()
	for product in product_list:
		run(product)
