

from setuptools import setup, find_packages


setup(name='FileShares',
    version='2.0.2',
    description='a simple way to sync files in team',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['termcolor'],
    entry_points={
    	'console_scripts': ['fshare=FileShares.run:main']
    },

)


