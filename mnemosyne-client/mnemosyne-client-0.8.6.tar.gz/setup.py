from setuptools import setup

setup(
	name='mnemosyne-client',
	version='0.8.6',
	description='mnemosyne service grpc client library',
	url='http://github.com/piotrkowalczuk/mnemosyne',
	author='Piotr Kowalczuk',
	author_email='p.kowalczuk.priv@gmail.com',
	license='MIT',
	packages=['mnemosynerpc'],
	install_requires=[
		'protobuf',
		'grpcio',
	],
  	zip_safe=False,
  	keywords=['mnemosyne', 'grpc', 'session', 'service', 'client'],
  	download_url='https://github.com/piotrkowalczuk/mnemosyne/archive/v0.8.5.tar.gz',
  )