from setuptools import setup

VERSION = "0.0.42"

setup(
	name = 'agent-for-sre',
	version = VERSION,
	description = 'The agent for sre',
	url = 'http://no.website/',
	author = 'niht',
	author_email = '5007088@qq.com',
	license = 'GPLv3',
	install_requires = [
		#'psutil',
#		'dnspython',
#		'pycurl',
#		'pyyaml',
#		'nsnitro'
	],
	packages = ['agent_for_sre'],
	package_data = {'agent_for_sre': ['*.py','Conf/*.py','Collector/*.py','Monitor/*.py']},
	scripts = [ "cli/check-url-callmap.py" ],
	zip_safe = False
)
