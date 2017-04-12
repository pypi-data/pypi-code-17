import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "minlp",
    version = "2",
    author = "SUNG MIN YANG",
    author_email = "sungmin.nlp@gmail.com",
    description = ("just test for now."),
    license = "GNU",
    keywords = "tutorial",
    url = "http://minteacher.com",
    packages=['inside_one', 'inside_two'],
    long_description=read('README'),
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
      'console_scripts': [
        'hello_world = inside_one:myfunc']
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