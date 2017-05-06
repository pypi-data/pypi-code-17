from setuptools import setup

try:
    import pypandoc
    long_descr = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_descr = open('README.md').read()

setup(name='movie_collection',
      version='0.1.1',
      description='Create dvd collection and calculate runtime',
      long_description=long_descr,
      classifiers=[
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
      ],
      keywords='movie library dvd length',
      author='Juliana Borst',
      author_email='j_borst1@pacific.edu',
      packages=['movie_collection'],
      test_suite='movie_collection.tests',
      include_package_data=True,
      zip_safe=False)
