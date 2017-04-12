import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "minlp",
    version = "3",
    author = "SUNG MIN YANG",
    author_email = "sungmin.nlp@gmail.com",
    description = ("just test for now."),
    license = "GNU",
    keywords = "tutorial",
    url = "http://minteacher.com",
    packages=find_packages(),
    long_description=read('README'),
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
      'console_scripts': [
        'min_func = inside_one.infile_one:myfunc']
    },
)



"""from setuptools import setup

setup(
   name='foo',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=['foo'],  #same as name
   install_requires=['bar', 'greek'], #external packages as dependencies
)
"""