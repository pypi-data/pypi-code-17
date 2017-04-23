"""Setup module for pyempt

See https://github.com/emin63/pyempt/blob/master/README.md for more
details of pyempt
"""

import codecs
import os
import re

from setuptools import setup

def make_dynamic_kwargs():
    """Make dynamically generated keyword args for setup.
    """
    kwargs = {}
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'),
                     encoding='utf-8') as fdesc:
        kwargs['long_description'] = fdesc.read()
    with codecs.open(os.path.join(here, 'pyempt', 'pyempt.py'),
                     encoding='utf-8') as fdesc:
        data = fdesc.read()
        vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
        vers = re.search(vsre, data, re.M)
        kwargs['version'] = vers.group(1)
    return kwargs

setup(
    name='pyempt',
    description='Python emacs syntax checking',
    url='https://github.com/emin63/pyempt',
    author='Emin Martinian',
    author_email='emin.martinian@gmail.com',
    license='BSD',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    keywords='continuous integration emacs development',

    packages=['pyempt'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    install_requires=['pylint', 'pep8'],
    extras_require={},
    data_files=[],
    package_data={
        'pyempt': ['pyempt/*'],
    },
    include_package_data=True,    
    entry_points={
        'console_scripts': [
            'pyempt=pyempt.pyempt:main'],
    },
    **make_dynamic_kwargs()
)
