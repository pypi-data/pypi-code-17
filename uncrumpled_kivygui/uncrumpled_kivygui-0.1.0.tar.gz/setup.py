from setuptools import setup, find_packages

setup(
    name = 'uncrumpled_kivygui',
    version='0.1.0',
    description = 'kivygui for uncrumpled',
    author='tmothy eichler',
    author_email='tim_eichler@hotmail.com',
    license='BSD',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3'],

    keywords = 'uncrumpled gui kivy ui',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)
