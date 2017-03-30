from distutils.core import setup

setup(name='ApiRepl',
      version='1',
      description='Elastic API to database worker framework.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Database',
                   'Intended Audience :: Developers',
                   'Programming Language :: SQL',
                   'Programming Language :: Python :: 2.7'],
      long_description=open('README.md', 'r').read(),
      packages=['ApiRepl'],
      )
