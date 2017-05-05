from setuptools import setup


setup(
    name = 'clira',
    packages = ['clira'], # this must be the same as the name above
    version = '0.1.3',
    description = 'Command line client for Jira',
    author = 'Paweł Jastrzębski',
    author_email = 'jastrzab5@gmail.com',
    url = 'https://gitlab.com/havk/clira', # use the URL to the github repo
    download_url = 'https://gitlab.com/havk/clira/repository/archive.tar.gz?ref=0.1.3', # I'll explain this in a second
    keywords = ['JIRA', 'jira', 'terminal', 'cli'], # arbitrary keywords
    classifiers = [],
    install_requires=[
        'jira==1.0.10'
        'click==6.7'
        'arrow==0.10.0'
    ],
    entry_points={
        'console_scripts': [
            'clira=clira.cli:cli'
        ]
    }
)
