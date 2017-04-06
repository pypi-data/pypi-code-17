from setuptools import setup
setup(
    name = 'majorityvoting',
    packages = ['majorityvoting'],
    version = '0.1.5',
    description = 'Majority Judgement Voting tool (fit for sklearn, etc.)',
    author = 'Tao Peter Wang',
    author_email = 'peterwangtao0@hotmail.com',
    url = 'https://github.com/TPeterW/Probabilistic-Majority-Voting',
    download_url = 'https://github.com/TPeterW/Probabilistic-Majority-Voting/tarball/0.1.5',
    keywords = ['majority voting', 'sklearn', 'machine learning', 'probability', 'majority judgement'],
    install_requires=[
          'numpy',
    ],
    classifiers = [],
)