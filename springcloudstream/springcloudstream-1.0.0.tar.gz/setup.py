from setuptools import setup, find_packages

setup(name='springcloudstream',
      version='1.0.0',
      #test_suite='tests',
      description='A module to support streaming with spring-cloud-stream',
      author='David Turanski',
      author_email='dturanski@pivotal.io',
      url = 'https://github.com/dturanski/springcloudstream',
      packages=find_packages(exclude=['tests', 'tests.*']),
      license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Apache Software License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      #install_requires=[],  # external packages as dependencies
      #tests_require=['mock', 'unittest2']
      )
