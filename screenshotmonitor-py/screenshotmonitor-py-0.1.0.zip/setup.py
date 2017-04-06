from setuptools import setup

setup(
    name='screenshotmonitor-py',
    version='0.1.0',
    install_requires=[
        'requests',
        'six',
    ],
    packages=[
        'screenshotmonitor',
    ],
    url='https://bitbucket.org/phistrom/screenshotmonitor_py',
    download_url='https://bitbucket.org/phistrom/screenshotmonitor_py/get/v0.1.0.zip',
    license='Apache',
    author='Phillip Stromberg',
    author_email='phillip@stromberg.me',
    description='Unofficial library for using v2 of the ScreenshotMonitor.com API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
    ],
)
