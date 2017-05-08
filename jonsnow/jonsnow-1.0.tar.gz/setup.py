from distutils.core import setup
from setuptools import find_packages

setup(
        name='jonsnow',
        version='1.0',
        description='A simple tool to run a shell command when files change.',
        long_description='''
jonsnow is a tool to make running unit tests, etc. easier. Run it in a separate
terminal from where you're doing your editing and it will run an arbitrary shell
comand whenever you change a file in a specified directory.

Usage:
   jonsnow ./fight_white_walkers.sh
   jonsnow -r ../ echo "You know nothing..."

Arguments:
-r, --root PATH: specify the root directory you want {} to format.
                 Defaults to the current working directory.
--rtp PATH: Set the runtime path of the command you want to execute
        ''',
        url='https://github.com/galbacarys/jonsnow',
        author='Gabriel Albacarys',
        author_email='nameless912@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Utilities',
            'Programming Language :: Python :: 3'
            ],
        keywords='development build buildtools automation',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'jonsnow = jonsnow:run'
                ]
            }
        )


