from distutils.core import setup

__version__ = '1.0.1'

setup(
    author='Kit Scribe',
    author_email='kit.scribe@protonmail.com',
    url='https://github.com/Kit-Scribe/pycolorize',
    name='pycolorize',
    version=__version__,
    py_modules=['pycolorize'],
    platforms='any',
    license=open('LICENSE').read(),
    description='colorized output with no broken color lines',
    long_description=open('README.md').read(),
        classifiers=
         [
             'Development Status :: 5 - Production/Stable',
             'Environment :: Console',
             'Intended Audience :: Developers',
             'Intended Audience :: System Administrators',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python',
             ]
        )
