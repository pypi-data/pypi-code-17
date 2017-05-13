# shelljob setup.py
import os,sys
from setuptools import setup

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

# https://bugs.launchpad.net/mortoray.com/+bug/1274176
try:
	import pypandoc
	desc = pypandoc.convert( 'README.md', 'rst' )
except Exception as e:
	desc = ''

def list_files(path):
	m = []
	for root, dirnames, filenames in os.walk(path):
		for filename in filenames:
			m.append(os.path.join(root, filename))
	return m
			
setup(
	name = 'shelljob',
	packages = [ 'shelljob' ],
	package_dir = {
		'': base_dir,
	},
	version = '0.5.6',
	description = 'Run multiple subprocesses asynchronous/in parallel with streamed output/non-blocking reading. Also various tools to replace shell scripts.',
	author = 'edA-qa mort-ora-y',
	author_email = 'eda-qa@disemia.com',
	url = 'https://pypi.python.org/pypi/shelljob',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Developers',
		'Environment :: Console',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Topic :: Terminals',
		'Topic :: System',
		'Topic :: Software Development :: Build Tools',
		],
	long_description = desc,
	package_data = { 
		'shelljob': [ base_dir + '/doc/*' ] 
	},
	license = 'GPLv3',
)
