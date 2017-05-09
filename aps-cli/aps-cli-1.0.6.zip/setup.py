from setuptools import setup,find_packages

PACKAGE = "apscli"
NAME = "aps-cli"
DESCRIPTION = "a simple aps-cli"
AUTHOR = "wangchang"
AUTHOR_EMAIL = "wangchang@zetyun.com"
setup(
    name=NAME,
    version='1.0.6',
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['requests','ConfigParser','argparse','prettytable'],
    entry_points={
        'console_scripts':[
            'aps-cli = apscli.apsCli:main',
    ],
    }
)
