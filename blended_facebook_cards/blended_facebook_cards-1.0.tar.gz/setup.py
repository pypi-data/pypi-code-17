from setuptools import setup

setup(name='blended_facebook_cards',
      version='1.0',
      description='Easy Facebook cards plugin for Blended',
      url='http://jmroper.com/blended/',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['facebook_cards'],
      install_requires=[
          'blended',
      ],
      zip_safe=False)
