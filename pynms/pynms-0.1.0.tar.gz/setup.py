import ast
import re
from distutils.core import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pynms/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(name='pynms',
      author='CYH',
      url='https://github.com/ourbest/pynms',
      author_email='chenyonghui@gmail.com',
      version=version,
      description='ali nms simple client',
      packages=['pynms'],
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      install_requires=['requests']
      )
