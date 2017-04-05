from setuptools import setup

setup(
    name='hexip',
    version='0.1',
    description='Tool to convert IPv4 address to hex. Useful for PXE boot config etc',
    url='http://github.com/theunsa/hexpi',
    author='Theuns Alberts',
    author_email='theunsa@gmail.com',
    license='MIT',
    packages=['hexip'],
    scripts=['scripts/hexip'],
    zip_safe=False
)



