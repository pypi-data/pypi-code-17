from setuptools import find_packages, setup

setup(
    name='pymailgunner',
    version='1.4',
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/pymailgunner',
    download_url='https://github.com/pschmitt/pymailgunner/archive/master.zip',
    description='A simple mailgun client - pymailgun fork with Python 3 support',
    packages=find_packages(),
    license='Apache license version 2.0',
    platforms='OS Independent',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment'
    ],
    install_requires='requests>=2.2.1'
)
