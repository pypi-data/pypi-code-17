from setuptools import setup, find_packages

DIRS_EXCLUDED = ['dist', 'build', 'docs', 'tests']

setup(
    name='swipt',
    packages=find_packages(exclude=DIRS_EXCLUDED),
    version='0.1.1',
    description='StoneWork Is Pedro Ten',
    author='StoneWork Solutions',
    author_email='dev@stoneworksolutions.net',
    url='https://github.com/stoneworksolutions/swipt',
    download_url='https://github.com/stoneworksolutions/swipt/tarball/0.1.1',
    keywords=['swipt', 'pedroten', 'stonework'],
    classifiers=[],
    install_requires=[],
)
