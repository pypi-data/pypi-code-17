from distutils.core import setup

setup(
    name = 'tsaw',
    packages = ['tsaw'],
    version = open("tsaw/VERSION").read().strip(),
    description = 'TSAW : Torrent Server API Wrapper.',
    long_description=open('README.md').read(),
    author = "Yec'han Laizet",
    author_email = 'y.laizet@bordeaux.unicancer.fr',
    url = 'https://github.com/ylaizet/tsaw',
    download_url = 'https://github.com/ylaizet/tsaw/archive/%s.tar.gz' % open("tsaw/VERSION").read().strip(),
    license = "GPL3",
    keywords = ['api', 'sequencer', 'Torrent server'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ]
)
