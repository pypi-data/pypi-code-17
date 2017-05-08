from distutils.core import setup

import dj

setup(name='py-dev-common',
      author='CYH',
      url='https://github.com/ourbest/py-dev-common',
      author_email='chenyonghui@gmail.com',
      version=dj.__version__,
      description='py-dev-common',
      packages=['dj'],
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      install_requires=['django'],
      )
