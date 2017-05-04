from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = ""#open(os.path.join(here, 'NEWS.txt')).read()


version = '1.0.0a2'

install_requires = [
    "numpy",
    "scipy",
    "termcolor",
    "six",
    "argh",
    "nose"
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='dwell',
    version=version,
    description="Some Python packages for fft, smoothing, gridding",
    long_description=README + '\n\n' + NEWS,
    keywords='',
    author='Christopher Lee',
    author_email='lee@aeolisresearch.com',
    url='http://christopherlee.co.uk',
    license='BSD',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   ],
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['dwell=dwell:main']
    }
)
