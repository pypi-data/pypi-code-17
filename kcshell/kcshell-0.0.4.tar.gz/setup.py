from setuptools import setup, find_packages

setup(
    name = 'kcshell',
    version = '0.0.4',
    packages = ['kcshell'],
    author = 'Rui Reis',
    author_email = 'rui@deniable.org',
    url = 'https://github.com/fdiskyou/kcshell',
    description = 'Simple Python3 based interactive assembly/disassembly shell for various architectures powered by Keystone/Capstone.',
    license = 'BSD',
    install_requires=[
        'keystone-engine',
        'capstone'
    ],
    keywords = ['assembler', 'disassembler'],
    classifiers = [
        'Topic :: Security',
        'Topic :: Software Development :: Assemblers',
        'Topic :: Software Development :: Disassemblers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Information Technology',
        'Natural Language :: English'
    ],
    entry_points={
        'console_scripts': [
            'kcshell = kcshell.kcshell:main',
        ]
    },
)
