#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class MachineInfoCollectoer(Collector):
	def __init__(self):
		next

	def getMachineInfoByIp(self,hostip):
		path = "/opt/hades_prod/hades/asset_web/hosts_run"
		try:
			import ansible.runner
			aa = ansible.runner.Runner(
				host_list = path,
				module_name = 'setup',
				pattern=hostip,
			)
			bb = aa.run()
			s_data = {}
			if len(bb['contacted'])==0:
				print(bb['dark'])
				s_data["error"]= json.dumps(bb['dark'])
				return s_data
			else:
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_serialnumber'):
					s_data["sn"] =  bb['contacted'][hostip]['ansible_facts']['facter_serialnumber']
				elif bb['contacted'][hostip]['ansible_facts'].has_key('ansible_product_serial'):
					s_data["sn"] =  bb['contacted'][hostip]['ansible_facts']['ansible_product_serial']
				else:
					s_data["error"] = "sn not found"
	
				s_data["machine_model"] = bb['contacted'][hostip]['ansible_facts']['ansible_product_name']
				s_data["cpu_n"]  = bb['contacted'][hostip]['ansible_facts']['ansible_processor_vcpus']
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_processor0'):
					str=bb['contacted'][hostip]['ansible_facts']['facter_processor0']
					str=str.replace('\s+',' ')
				else:
					str=bb['contacted'][hostip]['ansible_facts']['ansible_processor'][1]
				s_data["cpu_details"] = str
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_memorysize_mb'):
				   s_data["mem_total_size"]= int(float(bb['contacted'][hostip]['ansible_facts']['facter_memorysize_mb']))
				else:
					s_data["mem_total_size"]= int(bb['contacted'][hostip]['ansible_facts']['ansible_memtotal_mb'])
	
				if bb['contacted'][hostip]['ansible_facts']['ansible_devices'].has_key('vda'):
					s_data["d_total_size"] = "vda: "+bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['size']
	
					if bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['model'] == None:
						bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['model'] = ''
					s_data['d_details'] = bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['vendor'] + " " + bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['host'] + " " + bb['contacted'][hostip]['ansible_facts']['ansible_devices']['vda']['model']
				elif bb['contacted'][hostip]['ansible_facts']['ansible_devices'].has_key('sda'):
					if bb['contacted'][hostip]['ansible_facts']['ansible_devices'].has_key('sdb'):
						s_data["d_total_size"] = "sda: "+bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['size']+"   sdb: "+bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sdb']['size']
					else:
						s_data["d_total_size"] = "sda: "+bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['size']
					if bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['model'] == None:
						bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['model'] = ''
					s_data['d_details'] = bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['vendor'] + " " + bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['host'] + " " + bb['contacted'][hostip]['ansible_facts']['ansible_devices']['sda']['model']
				#CMDB 信息
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_hostname'):
					s_data['hostname'] = bb['contacted'][hostip]['ansible_facts']['facter_hostname']
				else:
					s_data['hostname'] = bb['contacted'][hostip]['ansible_facts']['ansible_hostname']
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_operatingsystem'):
					s_data['system_name'] = bb['contacted'][hostip]['ansible_facts']['facter_operatingsystem']
				else:
					s_data['system_name'] = bb['contacted'][hostip]['ansible_facts']['ansible_distribution']
				s_data['system_version'] = bb['contacted'][hostip]['ansible_facts']['ansible_distribution_version']
				if bb['contacted'][hostip]['ansible_facts'].has_key('facter_hardwaremodel'):
					s_data['system_arch'] = bb['contacted'][hostip]['ansible_facts']['facter_hardwaremodel']
				else:
					s_data['system_arch'] = bb['contacted'][hostip]['ansible_facts']['ansible_architecture']
				#NET 信息
				s_data['net'] = []
				net_data_type = 0
				for key in bb['contacted'][hostip]['ansible_facts']['ansible_interfaces']:
					if bb['contacted'][hostip]['ansible_facts'].has_key('ansible_' + key):
						if 'ipv4' in bb['contacted'][hostip]['ansible_facts']['ansible_' + key]:
							#if 'lo' not in  key:
							if 'eth' in key or 'bond' in key:
								net = {}
								if 'macaddress' in bb['contacted'][hostip]['ansible_facts']['ansible_' + key]:
									net['mac_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_' + key]['macaddress']
								net['ip_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_' + key]['ipv4']['address']
								net['mask_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_' + key]['ipv4']['netmask']
								net['gateway_address'] =  bb['contacted'][hostip]['ansible_facts']['ansible_default_ipv4']['gateway']
								net['device_name'] = key
								s_data['net'].append(net)
								net_data_type += 1
						else:
							net_data_type += 0
	
				if net_data_type == 0 :
					if bb['contacted'][hostip]['ansible_facts'].has_key('ansible_default_ipv4'):
						net = {}
						net['mac_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_default_ipv4']['macaddress']
						net['ip_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_default_ipv4']['address']
						net['mask_address'] = bb['contacted'][hostip]['ansible_facts']['ansible_default_ipv4']['netmask']
						net['gateway_address'] =  bb['contacted'][hostip]['ansible_facts']['ansible_default_ipv4']['gateway']
						net['device_name'] = 'default'
						s_data['net'].append(net)
	
	#			print s_data
			return s_data
		except ImportError:
			return
