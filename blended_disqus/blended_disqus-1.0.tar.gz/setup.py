from setuptools import setup

setup(name='blended_disqus',
      version='1.0',
      description='Easy Disqus plugin for Blended',
      url='http://jmroper.com/blended/',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['blended_disqus'],
      install_requires=[
          'blended',
      ],
      zip_safe=False)
