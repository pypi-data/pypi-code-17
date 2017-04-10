from distutils.core import setup

setup(name='bguo',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='File-based contact management',
      url='http://src.thomaslevine.com/bguo/',
      install_requires=[
          'horetu>=0.3.2',
      ],
      extras_require={
          'seltzer': 'lxml>=3.6.2',
      },
      packages=['bguo'],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      entry_points = {'console_scripts': ['bguo = bguo:main']},
      version='0.2.3',
      license='AGPL',
      )
