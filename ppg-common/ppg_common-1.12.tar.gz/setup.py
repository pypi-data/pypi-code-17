from setuptools import setup

setup(
    name='ppg_common',
    version='1.12',
    description='Clients',
    url='https://bitbucket.org/sbg-interns/ppg_common',
    author='Sbg Core Interns',
    author_email='strahinja.kovacevic994@gmail.com',
    install_requires=[
        'requests==2.13.0',
        'tornado==4.5',
        'PyYAML==3.12',
        'SQLAlchemy==1.1.9',
        'Jinja2==2.9.6'
    ],
    packages=[
        'ppg_common',
        'ppg_common.errors',
        'ppg_common.clients',
        'ppg_common.handlers',
        'ppg_common.config'
    ]
)
