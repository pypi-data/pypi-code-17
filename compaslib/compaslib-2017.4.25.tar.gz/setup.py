from setuptools import setup

setup( name='compaslib',
       version='2017.04.25',
       description='A library to read/convert COMPAS ECG measurement files',
       url='https://bitbucket.org/atpage/compaslib',
       author='Alex Page',
       author_email='alex.page@rochester.edu',
       license='MIT',
       packages=['compaslib'],
       install_requires=['numpy'],
       scripts=['bin/compas2csv'],
       keywords='COMPAS ECG EKG',
       zip_safe=False )
