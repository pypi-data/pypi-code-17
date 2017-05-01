from setuptools import setup

setup(name='snfilter',
    version='0.2',
    description='Spotter Network Filtered Feeds',
    url='https://github.com/stephanellis/snfilter',
    author='Stephan M Ellis',
    author_email='stephan.ellis@gmail.com',
    license='MIT',
    install_requires=[
        'click',
        'requests',
    ],
    packages=['snfilter'],
    entry_points='''
    [console_scripts]
    snfilter-cli=snfilter.scripts:cli
    ''',
    zip_safe=False)
