#!/usr/bin/python
# encoding: utf-8
from .Collector import Collector

class FirewallCollector(Collector):
	__ip=''
	__user=''
	__password=''
	def __init__(self,ip,username,password):
		self.__ip=ip
		self.__user=user
		self.__password=password

	def getUpstreamByFirewallip(self):
		next

	def GetM6Eip(self):
		ip=self.__ip
		user=self.__user
		password=self.__password
		random_file="/tmp/fw_"+random_str()
		print random_file
	
		ssh = pexpect.spawn('ssh -p 22 %s@%s' % (user,ip))
	
		try:
			i = ssh.expect(['password:', 'continue connecting(yes/no)?'], timeout=300)
			if i == 0:
				ssh.sendline(password)
			elif i == 1:
				ssh.sendline('yes')
				ssh.expect('password:')
				ssh.sendline(password)
			ssh.expect('> ')
			ssh.sendline('show configuration | display xml | no-more')
			f=open(random_file,"w")
			ssh.logfile = f
			ssh.expect('> ')
			ssh.sendline('q')
			f.close()
			os.system("/bin/sed -i 's/^show configuration.*//' "+random_file)
			os.system("/bin/sed -i 's/^{primary:node0}.*//' "+random_file)
			os.system("/bin/sed -i 's/^.*@JFW-P.*//' "+random_file)
		except pexpect.EOF:
			print "EOF"
		except pexpect.TIMEOUT:
			print "TIMEOUT"
		finally:
			ssh.close()
		params = []
		try:
			tree=etree.parse(random_file)
			root=tree.getroot()
			now_time = GetNowTime()
			for i in root.xpath("/rpc-reply/configuration/security/nat/destination/pool"):
				find=root.xpath("/rpc-reply/configuration/security/nat/destination/rule-set/rule/name[text()='"+i.xpath("name/text()")[0]+"']/..")
				for child in find:
					ipaddress = str(i.xpath("address/ipaddr/text()")[0])
					ipaddress =  ipaddress[:-3]
					eip = str(child.xpath("dest-nat-rule-match/destination-address/dst-addr/text()")[0])
					eip = eip[:-3]
					date = str(now_time)
					idc = 'M6'
					param = [eip,ipaddress,"",date,idc]
					if param not in params:
						params.append(param)
			print params
		except Exception,ex:
			print ex
		finally:
			os.remove(random_file)
			return params
	
	def getAllInfoByFirewallip(self):
		self.getUpstreamByFirewallip()
