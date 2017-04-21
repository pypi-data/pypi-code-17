from setuptools import setup
readme = open('README.rst').read()

setup(name='pycu',
      version='0.2.0',
      description='PyICU Wrapper',
      long_description=readme,
      url='http://github.com/meyt/pycu',
      author='Mahdi Ghane.g',
      license='MIT',
      keywords='pyicu icu localization internationalization i18n calendar locale',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development :: Internationalization',
          'Topic :: Software Development :: Localization',
          'Topic :: Software Development :: Libraries'
      ],
      install_requires=[
          'pyicu'
      ],
      packages=['pycu'],
      )



