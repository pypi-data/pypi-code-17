from setuptools import setup, find_packages

setup(name = 'sodapclient',
      version = '0.1.0',
      description = 'A simple OpenDAP client library',
      author = 'Systems Engineering & Assessment Ltd.',
      author_email = 'Marcus.Donnelly@sea.co.uk',
      url = 'https://bitbucket.org/sea_dev/sodapclient',
      license = 'MIT',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 3',
                     'Topic :: Scientific/Engineering'
                     ],
      keywords = ['OpenDAP',
                  'Environment',
                  'Science'
                  ],
      packages = find_packages(),
      install_requires = ['numpy >= 1.12',
                          'Django >= 1.9'
                          ],
      package_data = {'sodapclient.Examples':['proxyserver.txt'],
                      },
      )
