#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, xlrd, yaml
# from anad_dev import ecrypt, send_gmail
Lines_conf = """# configuration file
#   [...]: default value
#   'y': yes or on(switched), 'n': no or off

'char_include': 'days'                          # ['']
'char_exclude': ['8 ', '3 d']                   # ['']
'path_2do_it': 'sample'                         # [./]
'target_extensions': ['xls', 'xlsm', 'xlsx']
'write_out_2log_file': 'y'                      # 'y': yes to out.txt | 'n': w/o logging

# vvvvvv not implemented yet below vvvvvv
# 'target_extensions': ['xls', 'xlsm', 'xlsx', 'txt']
"""
Fl_log = 'out.txt'
class xlsrch(object):
	@staticmethod
	def get_default():
		return {
			'char_include': 'test',                          # required
			'char_exclude': ('tested', 'abcdef'),            # [('', )]
			'root_dir': '.'    # [./]
		}
	@staticmethod
	def mk_fl_conf(fl_out):
		with open(fl_out, 'w') as fl_2write:
			fl_2write.write(Lines_conf)
	@staticmethod
	def mk_params():
		fl_conf = 'xlsrch_conf.yaml'
		if not os.path.exists(fl_conf):
			xlsrch.mk_fl_conf(fl_conf)
			print('[info] made config file: {}'.format(fl_conf))
			print('         please edit this file to search as you like')
			sys.exit(0)
		try:
			with open(fl_conf, 'r') as data_in:
				params = yaml.load( data_in.read() )
		except:
			return xlsrch.get_default()
		return params
	@staticmethod
	def check_the_file(params, fl_in):
		book = xlrd.open_workbook(fl_in)
		# print('number of sheets / encoding / file name: {} / {}'.format(book.nsheets, book.encoding))
		flg_4log = params['write_out_2log_file']=='y'
		for (i, sheet) in enumerate( book.sheets() ):
			# print('{} {}x{}'.format(sheet.name, sheet.nrows, sheet.ncols))
			for num in range(sheet.nrows):
				values = sheet.row_values(num)
				for (k, val) in enumerate(values):
					if -1<str(val).find(params['char_include']):
						flg = True
						for word in params['char_exclude']:
							if -1<str(val).find(word): flg = False
						if flg:
							line_2write = '{}({}:{}, {}): {}'.format(fl_in, i+1, num+1, k+1, val)
							print(line_2write)
							if flg_4log:
								with open(Fl_log, 'a') as fl_out:
									fl_out.write('{}\n'.format(line_2write))
	@staticmethod
	def mk_search_root(params):
		ret = '.'
		path = params['path_2do_it']
		if not os.path.exists(path) or not os.path.isdir(path): return ret
		return os.path.abspath(path)
	@staticmethod
	def mk_fls(params):
		search_root = xlsrch.mk_search_root(params)
		print('[info] search_root: {}'.format(search_root))
		ret = []
		for searchpath, dirs, files in os.walk(search_root):
			for fl_name in files:
				for ext_ in params['target_extensions']:
					ext_2add = '' if ext_.find('.')==0 else '.'
					dot_ext = ext_2add+ext_
					splt = fl_name.split(dot_ext.lower())
					if 1<len(splt) and len(splt[-1])<1:
						print('{}/{}'.format(searchpath, fl_name))
						ret.append(os.path.join(searchpath, fl_name))
		return tuple(ret)
	@staticmethod
	def doIt():
		params = xlsrch.mk_params()
		if os.path.exists(Fl_log): os.remove(Fl_log)
		fls = xlsrch.mk_fls(params)
		print('[info] {} files has been found as same as the extensions.'.format(len(fls)))
		for fl_in in fls:
			xlsrch.check_the_file(params, fl_in)
		# print(params)
		# print('  char_exclude #01: {}'.format(params['char_exclude'][1]))
if __name__ == '__main__':
#	log = open('/home/dais/tmp/uwsgid/ws_ischm.log', 'a')
#	sys.stdout = log
	print('[info] test_it starting...')
	xlsrch.doIt()
