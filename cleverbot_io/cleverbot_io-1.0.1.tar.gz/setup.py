from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='cleverbot_io',
    version='1.0.1',
    packages=['cleverbot_io'],
	install_requires=['requests'],
	include_package_data=True,
    url='http://www.cleverbot.io',
    license='MIT',
    author='Underforest',
    author_email='neovisatoons@gmail.com',
    description='An unofficial Python wrapper for Cleverbot.io',
	long_description=read('README')
	)
