from setuptools import setup, find_packages

setup(
    name = 'pybot-adapter-slack',
    version = '0.0.2',
    description = "Slack adapter for pybot",
    url = 'https://github.com/jcomo/pybot-adapter-slack',
    author = 'Jonathan Como',
    author_email = 'jonathan.como@gmail.com',
    packages = find_packages(exclude=['docs', 'tests', 'scripts']),
    install_requires = ['slackclient'],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'python chat bot framework automation slack'
)
