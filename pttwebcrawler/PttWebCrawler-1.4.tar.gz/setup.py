from distutils.core import setup

setup(
    name = 'PttWebCrawler',
    packages = ['PttWebCrawler'],
    version = '1.4',
    description = 'ptt web crawler',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/david30907d/ptt-web-crawler',
    download_url = '',
    keywords = [],
    classifiers = [],
    license='MIT',
    install_requires=[
        'argparse',
        'beautifulsoup4',
        'requests',
        'six'
    ],
    entry_points={
        'console_scripts': [
            'PttWebCrawler = PttWebCrawler.__main__:main'
        ]
    },
    zip_safe=True
)
