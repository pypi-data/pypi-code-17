import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, 'vtools/version.txt')
version = open(version_path).read().strip()

requires = [ 'opencv-python>=3.0', 'numpy' ]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Telecommunications Industry',
    'Natural Language :: English',
    'Operating System :: Linux',
    'Operating System :: Windows',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Multimedia :: Video',
    'Topic :: Utilities',
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
]

# wsdl_files = [ 'wsdl/' + item for item in os.listdir('wsdl') ]

setup(
      name='vtools',
      version=version,
      description='Tools that I use frequently - Vic\'s Tools',
      long_description=open('README.rst', 'r').read(),
      author='Vic Jackson',
      author_email='mr.vic.jackson@gmail.com',
      maintainer='Vic Jackson',
      maintainer_email='mr.vic.jackson@gmail.com',
      license='MIT',
      keywords=['vtools', 'vimg' 'image processing', 'image', 'processing', 'BFS', 'DFS', 'Memoize', 'Tree'],
      url='https://github.com/etherwar/vtools',
      download_url='https://github.com/etherwar/vtools4/archive/vtools-0-0-2.tar.gz',
      zip_safe=False,
      packages=find_packages(exclude=['docs', 'examples', 'tests']),
      install_requires=requires,
      include_package_data=True,
     )




