from setuptools import setup, find_packages

setup(name='sillymap',
        version='0.1.0',
        description='A silly implementation of a short read mapper for the course DD3436.',
        url='http://github.com/alneberg/sillymap',
        author='Johannes Alneberg',
        author_email='alneberg@kth.se',
        license='MIT',
        packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        zip_safe=False,
        scripts=['bin/sillymap']
   )
