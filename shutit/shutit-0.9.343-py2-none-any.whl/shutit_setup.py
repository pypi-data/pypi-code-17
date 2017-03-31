"""
shutit.tk.setup (core ShutIt setup module)

Nomenclature:
    - Host machine:   Machine on which this script is run.
    - Target:         Environment to which we deploy (docker container, ssh, or bash shell)
    - Container:      Docker container created to run the modules on.

    - target_child    pexpect-spawned child created to build on target
    - host_child      pexpect spawned child living on the host machine
"""

# The MIT License (MIT)
# 
# Copyright (C) 2014 OpenBet Limited
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# ITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pexpect
import os
import time
import re
import logging
import shutit_pexpect
import shutit_global
from shutit_module import ShutItModule


class ShutItConnModule(ShutItModule):

	def __init__(self, *args, **kwargs):
		super(ShutItConnModule, self).__init__(*args, **kwargs)

	def setup_host_child(self):
		setup_host_child_environment(shutit_global.shutit)

	def setup_target_child(self, target_child, target_child_id='target_child',prefix='root'):
		setup_target_child_environment(shutit_global.shutit, target_child, target_child_id=target_child_id,prefix=prefix)
		


class ConnDocker(ShutItConnModule):
	"""Connects ShutIt to docker daemon and starts the container.
	"""

	def is_installed(self, shutit):
		"""Always considered false for ShutIt setup.
		"""
		return False

	def destroy_container(self, host_shutit_session_name, container_shutit_session_name, container_id, loglevel=logging.DEBUG):
		shutit = shutit_global.shutit
		host_child = shutit.get_shutit_pexpect_session_from_id(host_shutit_session_name).pexpect_child
		conn_docker_destroy_container(shutit, host_shutit_session_name, container_shutit_session_name, container_id, loglevel=loglevel)
		shutit.send(' command docker rm -f ' + container_id + ' && rm -f ' + shutit.build['cidfile'],shutit_pexpect_child=host_child,expect=shutit.expect_prompts['ORIGIN_ENV'],loglevel=loglevel)

	def start_container(self, shutit_session_name, loglevel=logging.DEBUG):
		return conn_docker_start_container(shutit_global.shutit, shutit_session_name, loglevel=loglevel)


	def build(self, shutit, loglevel=logging.DEBUG):
		"""Sets up the target ready for building.
		"""
		target_child = self.start_container('target_child', loglevel=loglevel)
		self.setup_host_child()
		# TODO: on the host child, check that the image running has bash as its cmd/entrypoint.
		self.setup_target_child(target_child)
		shutit.send('chmod -R 777 ' + shutit.build['shutit_state_dir'] + ' && mkdir -p ' + shutit.build['build_db_dir'] + '/' + shutit.build['build_id'], shutit_pexpect_child=target_child, echo=False, loglevel=loglevel)
		return True


	def finalize(self, shutit):
		"""Finalizes the target, exiting for us back to the original shell
		and performing any repository work required.
		"""
		# Finish with the target
		shutit.get_shutit_pexpect_session_from_id('target_child').sendline('exit')
		host_child = shutit.get_shutit_pexpect_session_from_id('host_child').pexpect_child
		shutit.set_default_shutit_pexpect_session(host_child)
		shutit.set_default_shutit_pexpect_session_expect(shutit.expect_prompts['ORIGIN_ENV'])
		shutit.do_repository_work(shutit.repository['name'], docker_executable=shutit.host['docker_executable'], password=shutit.host['password'])
		# Final exits
		host_child.sendline('rm -f ' + shutit.build['cidfile']) # Exit raw bash
		host_child.sendline('exit') # Exit raw bash
		return True


	def get_config(self, shutit):
		return True


class ConnBash(ShutItConnModule):
	"""Connects ShutIt to a machine via bash.
	Assumes no docker daemon available for tagging and pushing.
	"""

	def is_installed(self, shutit):
		"""Always considered false for ShutIt setup.
		"""
		return False

	def get_config(self, shutit):
		return True

	def build(self, shutit):
		"""Sets up the machine ready for building.
		"""
		shutit_pexpect_session = shutit_pexpect.ShutItPexpectSession('target_child','/bin/bash')
		target_child = shutit_pexpect_session.pexpect_child
		shutit_pexpect_session.expect(shutit.expect_prompts['base_prompt'].strip(), timeout=10)
		self.setup_host_child()
		self.setup_target_child(target_child)
		return True

	def finalize(self, shutit):
		"""Finalizes the target, exiting for us back to the original shell
		and performing any repository work required.
		"""
		# Finish with the target
		shutit.get_shutit_pexpect_session_from_id('target_child').sendline('exit')
		return True


class ConnSSH(ShutItConnModule):
	"""Connects ShutIt to a machine via ssh.
	Assumes no docker daemon available for tagging and pushing.
	"""

	def is_installed(self, shutit):
		"""Always considered false for ShutIt setup.
		"""
		return False

	def get_config(self, shutit):
		shutit.get_config(self.module_id, 'ssh_host', '')
		shutit.get_config(self.module_id, 'ssh_port', '')
		shutit.get_config(self.module_id, 'ssh_user', '')
		shutit.get_config(self.module_id, 'password', '')
		shutit.get_config(self.module_id, 'ssh_key', '')
		shutit.get_config(self.module_id, 'ssh_cmd', '')
		return True

	def build(self, shutit, loglevel=logging.DEBUG):
		"""Sets up the machine ready for building.
		"""
		cfg = shutit.cfg
		ssh_host = cfg[self.module_id]['ssh_host']
		ssh_port = cfg[self.module_id]['ssh_port']
		ssh_user = cfg[self.module_id]['ssh_user']
		ssh_pass = cfg[self.module_id]['password']
		ssh_key  = cfg[self.module_id]['ssh_key']
		ssh_cmd  = cfg[self.module_id]['ssh_cmd']
		opts = [
			'-t',
			'-o', 'UserKnownHostsFile=/dev/null',
			'-o', 'StrictHostKeyChecking=no'
		]
		if ssh_pass == '':
			opts += ['-o', 'PasswordAuthentication=no']
		if ssh_port != '':
			opts += ['-p', ssh_port]
		if ssh_key != '':
			opts += ['-i', ssh_key]
		host_arg = ssh_host
		if host_arg == '':
			shutit.fail('No host specified for sshing', throw_exception=False)
		if ssh_user != '':
			host_arg = ssh_user + '@' + host_arg
		cmd_arg = ssh_cmd
		if cmd_arg == '':
			cmd_arg = 'sudo su -s /bin/bash -'
		ssh_command = ['ssh'] + opts + [host_arg, cmd_arg]
		shutit.build['ssh_command'] = ' '.join(ssh_command)
		shutit.log('Startup command is: ' + shutit.build['ssh_command'],level=logging.INFO)
		shutit_pexpect_session = shutit_pexpect.ShutItPexpectSession('target_child', ssh_command[0], ssh_command[1:])
		target_child = shutit_pexpect_session.pexpect_child
		expect = ['assword', shutit.expect_prompts['base_prompt'].strip()]
		res = shutit.child_expect(target_child,expect, timeout=10)
		while True:
			shutit.log(target_child.before + target_child.after,level=logging.DEBUG)
			if res == 0:
				shutit.log('...',level=logging.DEBUG)
				res = shutit.send(ssh_pass, shutit_pexpect_child=target_child, expect=expect, timeout=10, check_exit=False, fail_on_empty_before=False, echo=False, loglevel=loglevel)
			elif res == 1:
				shutit.log('Prompt found, breaking out',level=logging.DEBUG)
				break
		self.setup_host_child()
		self.setup_target_child(target_child)
		return True

	def finalize(self, shutit):
		"""Finalizes the target, exiting for us back to the original shell
		and performing any repository work required.
		"""
		# Finish with the target
		shutit.get_shutit_pexpect_session_from_id('target_child').sendline('exit')
		shutit.set_default_shutit_pexpect_session(shutit.get_shutit_pexpect_session_from_id('host_child'))
		# Final exits
		host_child = shutit.get_shutit_pexpect_session_from_id('host_child').pexpect_child
		host_child.sendline('exit') # Exit raw bash
		return True


def conn_module():
	"""Connects ShutIt to something
	"""
	return [
		ConnDocker('shutit.tk.conn_docker', -0.1, description='Connect ShutIt to docker'),
		ConnSSH('shutit.tk.conn_ssh', -0.1, description='Connect ShutIt to a host via ssh'),
		ConnBash('shutit.tk.conn_bash', -0.1, description='Connect ShutIt to a host via bash'),
	]


class setup(ShutItModule):

	def is_installed(self, shutit):
		"""Always considered false for ShutIt setup.
		"""
		return False

	def build(self, shutit, loglevel=logging.DEBUG):
		"""Initializes target ready for build and updating package management if in container.
		"""
		if shutit.build['delivery'] in ('docker','dockerfile'):
			if shutit_global.shutit.get_current_shutit_pexpect_session_environment().install_type == 'apt':
				shutit.add_to_bashrc('export DEBIAN_FRONTEND=noninteractive')
				if not shutit.command_available('lsb_release'):
					shutit.install('lsb-release')
				shutit.lsb_release()
			elif shutit_global.shutit.get_current_shutit_pexpect_session_environment().install_type == 'yum':
				# yum updates are so often "bad" that we let exit codes of 1 through.
				# TODO: make this more sophisticated
				shutit.send('yum update -y', timeout=9999, exit_values=['0', '1'], loglevel=loglevel)
			shutit.pause_point('Anything you want to do to the target host ' + 'before the build starts?', level=2)
		return True

	def remove(self, shutit):
		"""Removes anything performed as part of build.
		"""
		return True

	def get_config(self, shutit):
		"""Gets the configured core pacakges, and whether to perform the package
		management update.
		"""
		return True



def module():
	return setup('shutit.tk.setup', 0.0, description='Core ShutIt setup')


def conn_docker_start_container(shutit, shutit_session_name, loglevel=logging.DEBUG):
	docker = shutit.host['docker_executable'].split(' ')
	# Always-required options
	if not os.path.exists(shutit.build['shutit_state_dir'] + '/cidfiles'):
		os.makedirs(shutit.build['shutit_state_dir'] + '/cidfiles')
	shutit.build['cidfile'] = shutit.build['shutit_state_dir'] + '/cidfiles/' + shutit.host['username'] + '_cidfile_' + shutit.build['build_id']
	cidfile_arg = '--cidfile=' + shutit.build['cidfile']
	# Singly-specified options
	privileged_arg   = ''
	name_arg         = ''
	hostname_arg     = ''
	rm_arg           = ''
	net_arg          = ''
	mount_docker_arg = ''
	shell_arg        = '/bin/bash'
	if shutit.build['privileged']:
		privileged_arg = '--privileged=true'
	if shutit.target['name'] != '':
		name_arg = '--name=' + shutit.target['name']
	if shutit.target['hostname'] != '':
		hostname_arg = '-h=' + shutit.target['hostname']
	if shutit.build['net'] != '':
		net_arg        = '--net="' + shutit.build['net'] + '"'
	if shutit.build['mount_docker']:
		mount_docker_arg = '-v=/var/run/docker.sock:/var/run/docker.sock'
	# Incompatible with do_repository_work
	if shutit.target['rm']:
		rm_arg = '--rm=true'
	if shutit.build['base_image'] in ('alpine','busybox'):
		shell_arg = '/bin/ash'
	# Multiply-specified options
	port_args         = []
	dns_args          = []
	volume_args       = []
	volumes_from_args = []
	volumes_list      = shutit.target['volumes'].strip().split()
	volumes_from_list = shutit.target['volumes_from'].strip().split()
	ports_list        = shutit.target['ports'].strip().split()
	dns_list          = shutit.host['dns'].strip().split()
	for portmap in ports_list:
		port_args.append('-p=' + portmap)
	for dns in dns_list:
		dns_args.append('--dns=' + dns)
	for volume in volumes_list:
		volume_args.append('-v=' + volume)
	for volumes_from in volumes_from_list:
		volumes_from_args.append('--volumes-from=' + volumes_from)

	docker_command = docker + [
		arg for arg in [
			'run',
			cidfile_arg,
			privileged_arg,
			name_arg,
			hostname_arg,
			rm_arg,
			net_arg,
			mount_docker_arg,
		] + volume_args + volumes_from_args + port_args + dns_args + [
			'-t',
			'-i',
			shutit.target['docker_image'],
			shell_arg
		] if arg != ''
	]
	shutit.build['docker_command'] = ' '.join(docker_command)
	# docker run happens here
	shutit.log('Startup command is: ' + shutit.build['docker_command'],level=logging.INFO)
	shutit.log('Downloading image, please be patient',level=logging.INFO)
	was_sent = ' '.join(docker_command)
	shutit_pexpect_session = shutit_pexpect.ShutItPexpectSession(shutit_session_name, docker_command[0], docker_command[1:])
	target_child = shutit_pexpect_session.pexpect_child
	expect = ['assword', shutit.expect_prompts['base_prompt'].strip(), 'Waiting', 'ulling', 'endpoint', 'Download','o such file']
	res = shutit_pexpect_session.expect(expect, timeout=9999)
	while True:
		if target_child.before == type(pexpect.exceptions.EOF):
			shutit.fail('EOF exception seen')
		try:
			shutit.log(target_child.before + target_child.after,level=logging.DEBUG)
		except:
			pass
		if res == 0:
			res = shutit.send(shutit.host['password'], shutit_pexpect_child=target_child, expect=expect, timeout=9999, check_exit=False, fail_on_empty_before=False, echo=False, loglevel=loglevel)
		elif res == 1:
			shutit.log('Prompt found, breaking out',level=logging.DEBUG)
			break
		elif res == 6:
			shutit.fail('Docker not installed.')
			break
		elif res == 7:
			shutit.log('Initial command timed out, assuming OK to continue.',level=logging.WARNING)
			break
		elif res == 8:
			shutit.fail('EOF seen.')
		else:
			res = shutit_pexpect_session.expect(expect, timeout=9999)
			continue
	shutit.log('Getting cid',level=loglevel)
	# Get the cid, to determine whether the container started up ok.
	# pexpect.spawn does not give us an easy way to determine the success of the run without closing the stream.
	while True:
		try:
			cid = open(shutit.build['cidfile']).read()
			break
		except Exception:
			time.sleep(1)
	if cid == '' or re.match('^[a-z0-9]+$', cid) == None:
		shutit.fail('Could not get container_id - quitting. Check whether other containers may be clashing on port allocation or name.\nYou might want to try running: sudo docker kill ' + shutit.target['name'] + '; sudo docker rm ' + shutit.target['name'] + '\nto resolve a name clash or: ' + shutit.host['docker_executable'] + ' ps -a | grep ' + shutit.target['ports'] + " | awk '{print $1}' | " + 'xargs ' + shutit.host['docker_executable'] + ' kill\nto ' + 'resolve a port clash\n')
	shutit.log('cid: ' + cid,level=logging.DEBUG)
	shutit.target['container_id'] = cid
	return target_child


def conn_docker_destroy_container(shutit, host_shutit_session_name, container_shutit_session_name, container_id, loglevel=logging.DEBUG):
	# Close connection.
	shutit.get_shutit_pexpect_session_from_id(container_shutit_session_name).pexpect_child.close()
	host_child = shutit.get_shutit_pexpect_session_from_id(host_shutit_session_name).pexpect_child
	shutit.send(' command docker rm -f ' + container_id + ' && rm -f ' + shutit.build['cidfile'],shutit_pexpect_child=host_child,expect=shutit.expect_prompts['ORIGIN_ENV'],loglevel=loglevel)


def setup_host_child_environment(shutit):
	# Now let's have a host_child
	shutit.log('Spawning host child',level=logging.DEBUG)
	shutit_pexpect_session = shutit_pexpect.ShutItPexpectSession('host_child', '/bin/bash')
	# Set up prompts and let the user do things before the build
	shutit.set_default_shutit_pexpect_session(shutit_pexpect_session)
	shutit.set_default_shutit_pexpect_session_expect(shutit.expect_prompts['base_prompt'])
	# ORIGIN_ENV is a special case of the prompt maintained for performance reasons, don't change.
	prefix = 'ORIGIN_ENV'
	shutit_pexpect_session.setup_prompt('ORIGIN_ENV', prefix=prefix)
	shutit_pexpect_session.login_stack_append(prefix)


def setup_target_child_environment(shutit, target_child, target_child_id='target_child',prefix='root'):
	# Some pexpect settings
	shutit_pexpect_session = shutit.get_shutit_pexpect_session_from_id(target_child_id)
	shutit_pexpect_session.pexpect_child = target_child
	shutit.set_default_shutit_pexpect_session_expect(shutit.expect_prompts['base_prompt'])
	# target child
	shutit.set_default_shutit_pexpect_session(shutit_pexpect_session)
	shutit_pexpect_session.setup_prompt(prefix,prefix=prefix)
	shutit_pexpect_session.login_stack_append(prefix)
