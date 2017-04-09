from distutils.core import setup

setup(
	name = 'product_tagger',
	version = '0.104',
	packages = ['product_tagger','product_tagger.resources'],
    package_data={'': ['*.pkl', '*.txt',]},
	url = 'https://github.com/nickyongzhang/product_tagger',
	license = 'MIT licenced',
	long_description = open('README.txt').read()
	)

