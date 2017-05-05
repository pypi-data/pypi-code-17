from distutils.core import setup
setup(
    name = 'clira',
    packages = ['clira'], # this must be the same as the name above
    version = '0.1.1',
    description = 'Command line client for Jira',
    author = 'Paweł Jastrzębski',
    author_email = 'jastrzab5@gmail.com',
    url = 'https://gitlab.com/havk/clira', # use the URL to the github repo
    download_url = 'https://gitlab.com/havk/clira/repository/archive.tar.gz?ref=0.1.1', # I'll explain this in a second
    keywords = ['JIRA', 'jira', 'terminal', 'cli'], # arbitrary keywords
    classifiers = [],
)
