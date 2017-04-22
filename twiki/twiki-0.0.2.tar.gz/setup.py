from setuptools import setup, find_packages

version = "0.0.2"

long_description = ""
try:
    long_description = file('README.md').read()
except Exception:
    pass

license = ""
try:
    license = file('LICENSE').read()
except Exception:
    pass


setup(
    name='twiki',
    version=version,
    description='A bunch of tools which allow manage a TWiki',
    author='Pablo Saavedra',
    author_email='psaavedra@igalia.com',
    url='http://github.com/psaavedra/python-twiki',
    packages=find_packages(),
    package_data={
    },
    scripts=[
        "tools/twiki-get-topics",
        "tools/twiki-move-topic",
        "tools/twiki-rename-topic",
    ],
    zip_safe=False,
    install_requires=[
        "requests",
    ],
    data_files=[
        ('/usr/share/doc/twiki-actions/',
            ['cfg/twiki.cfg.example']),
    ],

    download_url='https://github.com/psaavedra/python-twiki/zipball/master',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
    ],
    long_description=long_description,
    license=license,
    keywords="python twiki csv",
)
