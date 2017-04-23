from setuptools import setup, find_packages

setup(
    name='rorocloud',
    version='0.1.2',
    author='rorodata',
    author_email='rorodata.team@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'requests==2.13.0',
        'web.py>=0.40.dev'
    ],
    entry_points='''
        [console_scripts]
        rorocloud=rorocloud.cli:main
        rorocloud-dev=rorocloud.cli:main_dev
    ''',
)
