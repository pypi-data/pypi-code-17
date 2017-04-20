from setuptools import Command, setup, find_packages

# see StackOverflow/458550
exec(open('src/pycel/version.py').read())

setup(name='pycel-x',
      version='3.'+__version__,
      packages=find_packages('src'),
      package_dir = {'':'src'},
      description='A library for compiling excel spreadsheets to python code & visualizing them as a graph',
      url = 'https://github.com/dgorissen/pycel',
      tests_require = ['nose >= 1.2'],
      test_suite='nose.collector',
      install_requires = ['networkx', 
                          'openpyxl'
                          ],
      author='Dirk Gorissen + CERN',
      author_email='zern.exz@gmail.com',
      long_description = """\
Pycel3 is a small python library that can translate an Excel spreadsheet into executable python code which can be run independently of Excel. The python code is based on a graph and uses caching & lazy evaluation to ensure (relatively) fast execution. The graph can be exported and analyzed using tools like Gephi. See the contained example for an illustration.
""",
      classifiers =[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ]
      )

