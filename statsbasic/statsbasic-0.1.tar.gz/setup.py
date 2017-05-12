from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='statsbasic',
      version='0.1',
      description='Run Basic Statistical Test with lots of output - emphasys on Learning',
      url='http://github.com/',
      author='Diego',
      author_email='dmenin@gmail.com',
      license='MIT',
      packages=['statsbasic'],
      install_requires=[
          'tabulate',
      ],
      zip_safe=False)