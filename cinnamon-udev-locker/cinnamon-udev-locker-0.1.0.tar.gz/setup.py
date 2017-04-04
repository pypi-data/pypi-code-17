import io
import setuptools

setuptools.setup(
    name='cinnamon-udev-locker',
    version='0.1.0',
    url='https://github.com/fladi/cinnamon-udev-locker',
    author='Michael Fladischer',
    author_email='michael@fladi.at',
    description='Lock Cinnamon desktop session on device removal (i.e YubiKey)',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'click',
        'click-log',
        'pygobject',
        'pyxdg',
    ],
    entry_points={
        'console_scripts': [
            'cinnamon-udev-locker = cinnamon_udev_locker.main:locker',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Desktop Environment :: Screen Savers',
        'Topic :: Security',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
