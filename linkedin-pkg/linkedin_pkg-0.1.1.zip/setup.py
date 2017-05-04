from setuptools import setup

try:
    import pypandoc
    long_descr = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_descr = open('README.md').read()

setup(name='linkedin_pkg',
      version='0.1.1',
      description='Create a LinkedIn account with a searchable network',
      long_description=long_descr,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
      ],
      keywords='networking social',
      author='Alex Katona',
      packages=['linkedin_pkg'],
      test_suite='linkedin_pkg.tests',
      include_package_data=False,
      zip_safe=False)
