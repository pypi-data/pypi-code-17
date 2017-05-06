from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name='rkn',
      version='0.1',
      description='Check domain/ip address in http://eais.rkn.gov.ru/ database',
      long_description=readme(),
      url='https://bitbucket.org/pi11/rkncheck/',
      author='pi11',
      author_email='co@defun.co',
      license='MIT',
      packages=['rkn'],
      install_requires=[
          'requests', 'antigate', 'pyquery',
      ],
      zip_safe=False)
