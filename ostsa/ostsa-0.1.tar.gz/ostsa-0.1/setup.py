# Setup file needed for distribution on PyPI.
#
# See the following blog post for a quick guide:
#
#     http://peterdowns.com/posts/first-time-with-pypi.html
#

from setuptools import setup

# Retrive the list of requirements from requirements.txt.
import inspect
import os.path

directory = os.path.dirname(inspect.getfile(inspect.currentframe()))
path = os.path.join(directory, 'requirements.txt')

with open(path) as file:
    requirements = file.read().split()

# Setup function
setup(name='ostsa',
      packages=['ostsa'],
      version='0.1',
      description=('A library for classifying malware files. This library '
                   'also contains various utilities for extending/building '
                   'your own specialized machine learning classifiers.'),
      author='Caleb Rush, Austin Julio, Andy Zheng',
      author_email='cir5274@psu.edu',
      url='https://github.com/psb-seclab/malware_classifier',
      download_url='https://github.com/psb-seclab/malware_classifier/archive/0.1.tar.gz',
      keywords=['machine learning', 'malware', 'pe', 'exe', 'dll', 
                'classifier', 'security', 'analysis'],
      install_requires=requirements)