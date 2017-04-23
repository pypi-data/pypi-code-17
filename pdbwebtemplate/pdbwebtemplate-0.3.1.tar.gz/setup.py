from setuptools import setup

setup(name='pdbwebtemplate',
      version='0.3.1',
      description='Template Model for web projects',
      url='https://Ferraresi@gitlab.com/promodebolso/pdbwebtemplate.git',
      author='Richard Ferraresi',
      author_email='richard@promodebolso.com.br',
      license='Comercial',
      packages=['pdbwebtemplate/core'],
      setup_requires=['setuptools-git'],
      zip_safe=True)