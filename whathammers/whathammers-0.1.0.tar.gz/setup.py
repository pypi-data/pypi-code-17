from setuptools import setup, find_packages

setup(
    name='whathammers',
    version='0.1.0',
    description='Command line tool for quick analysis of Apache log files',
    url='https://gitlab.com/aliceh75/whathammers',
    author='Alice Heaton',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='apache logfile analysis',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'apache-log-parser'
    ],
    entry_points='''
        [console_scripts]
        whathammers=whathammers.whathammers:main
    '''
)
