import os
from setuptools import setup

# commodore
# Manage and maintain your user's scripts and tools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="commodore",
    version="0.1.3",
    description="Manage and maintain your user's scripts and tools",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3+",
    keywords="",
    url="https://www.bitbucket.org/johannestaas/commodore",
    packages=['commodore'],
    package_dir={'commodore': 'commodore'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=['confutil', 'inter'],
    entry_points={
        'console_scripts': [
            'commodore=commodore:main',
        ],
    },
)
