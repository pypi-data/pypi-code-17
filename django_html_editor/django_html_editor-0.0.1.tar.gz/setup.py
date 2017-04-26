from distutils.core import setup 
from setuptools import find_packages

setup(name='django_html_editor',
      version='0.0.1',
      description='HTML source code editor widget based on CodeMirror JS plugin for Django admin.',
      author='Petr Dovnar',
      author_email='petrdovnar@gmail.com',
      url='https://github.com/python33/django_html_editor',
      packages=['html_editor'],
      include_package_data=True,
      zip_safe=False
     )

