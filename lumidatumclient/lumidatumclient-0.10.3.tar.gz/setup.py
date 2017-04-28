import distutils.core


distutils.core.setup(
    name='lumidatumclient',
    packages=['lumidatumclient'],
    version='0.10.3',
    description='A client for the Lumidatum REST API.',
    author='Mat Lee',
    author_email='matt@lumidatum.com',
    url='https://www.lumidatum.com',
    download_url='',
    keywords=['REST', 'machine learning'],
    classifiers=[],
    install_requires=[
        'requests',
        'requests-toolbelt',
    ]
)
