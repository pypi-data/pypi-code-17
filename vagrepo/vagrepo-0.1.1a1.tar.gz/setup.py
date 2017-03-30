import setuptools

setuptools.setup(
    name='vagrepo',
    description='A local vagrant box repository manager.',
    keywords='Vagrant repository Vagrant-boxes',
    version='0.1.1a1',
    url='https://github.com/matthijsbos/vagrepo',
    author='Matthijs Bos',
    author_email='matthijs_vlaarbos@hotmail.com',
    license='Apache License 2.0',
    install_requires=[],
    packages=['vagrepo'],
    entry_points={
        'console_scripts': [
            'vagrepo=vagrepo:main'
        ]
    },
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
