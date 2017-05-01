from setuptools import setup

setup(name='dnalearn',
      version='0.2',
      description='Recommender system for sequence design and optimization',
      url='https://github.com/tamimeur/DNAlearn.git',
      author='Leli Ami',
      author_email='tamimeur@gmail.com',
      license='MIT',
      packages=['dnalearn'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'pandas','numpy','click','keras==1.2','sklearn','scipy','xlrd','h5py',
      ],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'dnalearn = dnalearn.cli:main',
        ],
      })
