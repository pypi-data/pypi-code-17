from setuptools import setup


setup(name='qcos_cli',
      version='0.1',
      description='qcos python sdk cli wrapper',
      author='AnyISalIn',
      author_email='anyisalin@gmail.com',
      url='https://github.com/AnyISalIn/qcos_cli',
      packages=['qcos_cli'],
      install_requires=[
          'qcloud-cos-v4==0.0.18'
      ],
      entry_points={
          'console_scripts': [
              'qcos_cli=qcos_cli.cli:main'
          ]},
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ])
