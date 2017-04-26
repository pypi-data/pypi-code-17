from setuptools import setup

setup(name='twosampyle',
      version='0.1.8',
      description='Python module for two-sample statistical tests',
      url='https://github.com/jwilber/twosampyle',
      author='Jared Wilber',
      author_email='jdwlbr@gmail.com',
      license='GNU3',
      packages=['twosampyle'],
      install_requires=[
            'pandas',
            'numpy',
            'matplotlib',
            'scipy'
      ],
      zip_safe=False)
