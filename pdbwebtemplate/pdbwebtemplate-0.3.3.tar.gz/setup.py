from setuptools import setup

setup(name='pdbwebtemplate',
      version='0.3.3',
      description='Template Model for web projects',
      url='https://Ferraresi@gitlab.com/promodebolso/pdbwebtemplate.git',
      author='Richard Ferraresi',
      author_email='richard@promodebolso.com.br',
      license='Comercial',
      packages=['pdbwebtemplate/core', 'pdbwebtemplate/core/api', 'pdbwebtemplate/core/business',
                'pdbwebtemplate/core/models', 'pdbwebtemplate/core/spi'],
      setup_requires=['setuptools-git'],
      zip_safe=True)