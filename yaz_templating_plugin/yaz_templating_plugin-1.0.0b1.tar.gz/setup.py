from setuptools import setup

setup(name='yaz_templating_plugin',
      version='1.0.0b1',
      description='A templating plugin for YAZ',
      author='Boudewijn Schoon',
      author_email='yaz@frayja.com',
      license='MIT',
      packages=['yaz_templating_plugin'],
      install_requires=['yaz', 'jinja2', 'colored'],
      zip_safe=False)
