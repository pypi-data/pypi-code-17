from os.path import dirname, join
from setuptools import setup, find_packages

setup(
    name='LitMath',
    version='0.1.0',
    url='https://github.com/wangyao1052/PyLitMath',
    description='A simple 2D and 3D math library for Python.',
    long_description=open('README.md').read(),
    author='Hisin Wang',
    author_email="wangyao1052@163.com",
    maintainer='Hisin Wang',
    maintainer_email='wangyao1052@163.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
    ],
)