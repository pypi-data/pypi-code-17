from setuptools import setup

setup(name='latest_repo',
      version='0.1',
      description='Get latest repository of any GitHub user or organisation',
      url='http://github.com/storborg/funniest',
      author='Marta Zaryn',
      author_email='martazaryn@gmail.com',
      license='MIT',
      packages=['latest_repo'],
      long_description=open('README.md').read(),
      zip_safe=False)
