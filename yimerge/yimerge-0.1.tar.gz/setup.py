from distutils.core import setup

setup(
    name = 'yimerge',
    packages = ['yimerge'],
    version = '0.1',
    description = 'Dashcam footage concatenator',
    author = 'Przemysław Spodymek',
    author_email = 'przemyslaw@spodymek.com',
    url = 'https://github.com/spodym/yimerge',
    download_url = 'https://github.com/spodym/yimerge/archive/0.1.tar.gz',
    keywords = ['dashcam', 'cam', 'footage', 'concatenate', 'merge'],
    classifiers = [],
    entry_points = {
        'console_scripts': ['yimerge=yimerge.yimerge:main'],
    },
    install_requires=[
        'moviepy==0.2.2.13',
        'scipy==0.18.1',
    ],
)
