from distutils.core import setup
setup(
    name = 'markout',
    version = '0.7',
    description = 'Print Your Output using markdown beautifully!',
    author = 'Samuel Mueller',
    author_email = 'samuel.g.mueller@web.de',
    url = 'https://github.com/SamuelGabriel/markout', # use the URL to the github repo
    download_url = 'https://github.com/SamuelGabriel/markout/archive/0.7.tar.gz', # I'll explain this in a second
    keywords = ['testing', 'logging', 'markdown', 'beatiful'], # arbitrary keywords
    classifiers = [],
    install_requires=['markdown2'],
    entry_points={
        'console_scripts': [
            'markout=markout',
        ],
    },)