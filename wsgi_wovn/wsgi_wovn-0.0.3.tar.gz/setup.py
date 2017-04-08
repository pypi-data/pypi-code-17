from setuptools import find_packages
from setuptools import setup

README = open('README').read()

setup(name='wsgi_wovn',
      packages=find_packages(),
      version='0.0.3',
      description='WSGI middleware for translating application by WOVN.io. A port of wovnjava.',
      long_description=README,
      author='Masahiro IUCHI',
      author_email='masahiro.iuchi@gmail.com',
      url='https://github.com/masiuchi/wsgi-wovn',
      license='MIT License',
      keywords='wsgi middleware wovn',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP :: WSGI',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
          'Topic :: Software Development :: Internationalization',
          'Topic :: Software Development :: Localization',
      ],
      test_suite='tests',
      )
