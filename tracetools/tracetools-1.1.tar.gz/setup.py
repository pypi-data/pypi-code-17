from setuptools import setup

setup(name='tracetools',
      version='1.1',
      
      description='Trace toolkit to print formatted traces of binary data',
      long_description=open('README').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='trace hex',
      
      url='https://github.com/timgabets/tracetools',
      author='Tim Gabets',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['tracetools'],
      install_requires=[],
      zip_safe=True)