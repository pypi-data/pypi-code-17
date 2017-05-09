from distutils.core import setup

__version__ = '1.1.41'

setup(
    author='Kit Scribe',
    author_email='kit.scribe@protonmail.com',
    url='https://github.com/Kit-Scribe/sclogger.git',
    name='sclogger',
    version=__version__,
    py_modules=['sclogger'],
    platforms='any',
    license=open('LICENSE').read(),
    description='simple colorized logger',
    long_description=open('README.md').read(),
    requires=['pycolorize'],
        classifiers=
         [
             'Development Status :: 5 - Production/Stable',
             'Environment :: Console',
             'Intended Audience :: Developers',
             'Intended Audience :: System Administrators',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python',
             'Topic :: Software Development :: Debuggers',
             ]
    )
