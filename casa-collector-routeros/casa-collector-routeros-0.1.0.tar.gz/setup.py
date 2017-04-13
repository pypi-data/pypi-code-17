from distutils.core import setup

setup(
    name='casa-collector-routeros',
    version='0.1.0',
    author='Lewis Eason',
    author_email='me@lewiseason.co.uk',
    packages = ['casa_collector_routeros'],
    entry_points={
        'console_scripts': [
            'casa-collector-routeros = casa_collector_routeros.collector:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
