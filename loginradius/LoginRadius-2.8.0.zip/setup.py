from distutils.core import setup
setup(
    name = 'LoginRadius',
    py_modules = ['LoginRadius','UserRegistration'],
    version = '2.8.0',
    description = 'Social Login and User Registration for Python.',
    author='LoginRadius',
    author_email='developers@loginradius.com',
    url='http://loginradius.com/',
    classifiers=['Programming Language :: Python', 'Programming Language :: Python :: 2.7','Programming Language :: Python :: 3.6',
                 'Operating System :: OS Independent', 'License :: OSI Approved :: MIT License',
                 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers',
                 'Topic :: Internet', 'Topic :: Internet :: WWW/HTTP','Topic :: Software Development :: Libraries :: Python Modules'
                 ],
    keywords=['sociallogin', 'userregistration'],
)
