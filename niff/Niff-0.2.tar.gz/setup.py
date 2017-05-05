

from setuptools import setup, find_packages


setup(name='Niff',
    version='0.2',
    description='a tool',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['termcolor','requests'],
    entry_points={
        'console_scripts': ['Niff=Niff.main:main']
    },

)


