# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.MD') as f:
        return f.read()
    
setup(name='jmail',
      version='0.1.0.4',
      description='Simple mail lib4u',
      long_description=readme(),
      url='https://github.com/jiajie999/jmail',
      author='jiajie999',
      author_email='jiajie999@gmail.com',
      license='MIT',
      packages=['jmail'],
      install_requires=[
          'click',
          # Colorama is only required for Windows.
          'colorama',
      ],
      entry_points={
          'console_scripts': ['jmail=jmail.util:send'],
      },
      include_package_data=True,
      zip_safe=False)

