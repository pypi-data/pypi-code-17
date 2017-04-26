try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Wrapper',
    packages=['wrapper'],
    version='1.1.0-beta.1',
    license="GPL",
    description='''
    
    A wrapper around several APIs.
    
    Response is a request object, which is much extendable for custom error handling.
    
    The Available APIs are:
    
        EANData
        Locu
        Spoonacular
        Walmart
        Zomato

    
    
    ''',
    author='Biwin John',
    author_email='biwinjohn@gmail.com',
    url='https://github.com/biwin/wrapper',
    download_url='https://github.com/biwin/wrapper/archive/0.1.tar.gz',
    install_requires=[],
    requires=['requests', 'barcodenumber'],
    keywords=['api', 'python'],
    classifiers=[],
)
