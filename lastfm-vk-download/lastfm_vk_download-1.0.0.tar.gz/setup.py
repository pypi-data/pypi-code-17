#!/usr/bin/env python

from setuptools import setup

setup(
    name='lastfm_vk_download',
    version='1.0.0',
    description="Get user's top tracks from lastfm and download them from vk.com",
    author='Philip Blagoveschensky',
    author_email='me@crabman.me',
    url='https://github.com/philip-bl/lastfm_vk_download',
    packages=['lastfm_vk_download'],
    package_data={
        "lastfm_vk_download": ["decode.js", "vkfindaudio-w3m", "urlencode", "htmldecode"]},
    license='MIT',
    install_requires=[
        "click>=6.7",
        "requests>=2.13",
        "wget>=3.2",
        "plumbum>=1.6.3",
        "path.py>=10.1",
        "libcrap>=0.2.4"],
    entry_points="""
        [console_scripts]
        lastfm_to_json=lastfm_vk_download.lastfm_to_json:save_tracks
        download_from_vk=lastfm_vk_download.download_from_vk:main
    """,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        "Development Status :: 4 - Beta",
        'Topic :: Utilities'])
