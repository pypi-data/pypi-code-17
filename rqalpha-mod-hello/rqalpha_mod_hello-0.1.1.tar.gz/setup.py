from os.path import dirname, join
from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


with open(join(dirname(__file__), 'rqalpha_mod_hello/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()
    """
        作为一个合格的mod，应该要有版本号哦。
    """
setup(
    name='rqalpha_mod_hello',  #mod的名字
    version=version,
    description='A mod for RQAlpha to say hello',
    packages=find_packages(exclude=[]),
    author='yourname',
    author_email='your@email.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='https://github.com/johnsonchak/rqalpha-mod-hello/tree/master',
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],#所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
