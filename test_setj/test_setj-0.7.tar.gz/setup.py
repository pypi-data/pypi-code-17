from setuptools import setup

setup(name='test_setj',
      version='0.7',
      description='Demo python package for testing how setuptools work',
      long_description="Supposed to be long description of the package on PYPI. Version 0.7",
      url='https://github.com/apatniv/test_setj',
      author='vivek',
      author_email='apatniv@gmail.com',
      license='MIT',
      packages=['test_setj'],
      install_requires=[  # all the dependency modules required for this modules
            'markdown'
      ],
      zip_safe=False)