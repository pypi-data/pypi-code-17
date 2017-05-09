#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, yaml
from subprocess import PIPE, check_output
from timer import timer
# from anad_dev import ecrypt, send_gmail
Lines_conf = """# configuration file
#   [...]: default value
#   'y': yes or on(switched), 'n': no or off

'exec_sqlplus': 'sqlplus -s'
'uri_oracle': 'u/p@ip/s'
'sql':
  - |
    select count(*) from test
      where xx='yy';
  - |
    select * from test
      where xx='yy';
'safety_counts': 100000
'safety_seconds': 2
'file_name_out': 'out.txt'

# vvvvvv not implemented yet below vvvvvv
"""
Fl_log = 'out.txt'
Fl_sql = 'silent.sql'
Chr_splitter = '|||'
class oracler(object):
	@staticmethod
	def mk_login_sql():
		fl_out = 'login.sql'
		if os.path.exists(fl_out): return
		with open(fl_out, 'w') as fl_2write:
			fl_2write.write("""-- set newpage none
set term off
set pagesize 0
set head off
set feed off
set linesize 5000
set trimspool on
set colsep {}
""".format(Chr_splitter)		)
	@staticmethod
	def mk_fl_conf(fl_out):
		with open(fl_out, 'w') as fl_2write:
			fl_2write.write(Lines_conf)
	@staticmethod
	def mk_params():
		oracler.mk_login_sql()
		fl_conf = 'oracler_conf.yaml'
		if not os.path.exists(fl_conf):
			oracler.mk_fl_conf(fl_conf)
			print('[info] made config file: {}'.format(fl_conf))
			print('         please edit this file to use this oracler.py')
			sys.exit(0)
		try:
			with open(fl_conf, 'r') as data_in:
				params = yaml.load( data_in.read() )
		except:
			print('[err] could not read config file: {}'.format(fl_conf))
			sys.exit(0)
		return params
	@staticmethod
	def mk_ddl(params, sql):
		print('  sql:')
		print(sql)
		with open(Fl_sql, 'w') as fl_2write:
			fl_2write.write("""spool silent.log
{}
spool off
quit
""".format(sql)
			)
		with timer() as tmr:
			try:
				res = check_output('''{} "{}" "@{}"'''.format(params['exec_sqlplus'], params['uri_oracle'], Fl_sql),
						shell=True).decode('utf-8').strip()
				'''
				sqlplus -s "u/p@ip/s" "@silent.sql"
				res = check_output("cd {} && hg pull".format(dir_target), shell=True).decode('utf-8').strip()
				'''
			except:
				print('[err] could not execute command:')
				print('    ', end='')
				print('''{} "{}" "@{}"'''.format(params['exec_sqlplus'], params['uri_oracle'], Fl_sql) )
		cnt_msec = int(tmr.msecs)
		fl_log = 'silent.log'
		if not os.path.exists(fl_log):
			splt = []
		else:
			with open(fl_log, 'r') as fl_in:
				splt = fl_in.read().split('\n')
		return (cnt_msec, len(splt))
	@staticmethod
	def doIt():
		params = oracler.mk_params()
		if os.path.exists(Fl_log): os.remove(Fl_log)
		if len(params['sql'])<1 or len(params['sql'][-1])<1:
			print('[err] there is no sql to execute. please set the config file..')
			sys.exit(0)
		for sql in params['sql']:
			res = oracler.mk_ddl(params, sql)
			print(' (sql m seconds, response line size): ', end='')
			print(res)
			if params['safety_seconds']*1000<res[0] or params['safety_counts']<res[1]:
				print('[warn] for safety, the count number has been over the limit.')
				print('[warn]    will be exit the loop..')
				exit(0)
				
if __name__ == '__main__':
#	log = open('/home/dais/tmp/uwsgid/ws_ischm.log', 'a')
#	sys.stdout = log
	print('[info] test_ doIt starting...')
	oracler.doIt()
