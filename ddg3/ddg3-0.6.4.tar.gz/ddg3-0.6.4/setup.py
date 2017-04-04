from setuptools import setup

long_description = open('README.rst').read()

setup(
      name='ddg3',
      version='0.6.4',
      py_modules=['ddg3'],
      description='Library for querying the Duck Duck Go API, updated for python3',
      author='Michael Stephens, Jacobi Petrucciani',
      author_email='jacobi@mimirhq.com',
      license='BSD',
      url='https://github.com/jpetrucciani/python-duckduckgo',
      long_description=long_description,
      platforms=['any'],
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
      ],
      entry_points={'console_scripts': ['ddg3 = ddg3:main']},
)
