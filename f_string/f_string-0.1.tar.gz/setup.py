from distutils.core import setup
setup(
    name='f_string',
    packages=['f_string'],  # this must be the same as the name above
    version='0.1',
    description="This is fake version of python3.6's 'f_string' to use it in previous version of python3.6",
    author='davidcho',
    author_email='csi00700@gmail.com',
    keywords=['f_string', 'string'],  # arbitrary keywords
    install_requires=[
        'parse',
    ],
)
