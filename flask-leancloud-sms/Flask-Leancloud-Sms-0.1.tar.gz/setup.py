from setuptools import setup

setup(
    name='Flask-Leancloud-Sms',
    version='0.1',
    url='http://github.com/n0trace/flask-leancloud-sms/',
    license='MIT',
    author='n0trace',
    author_email='n0trace@protonmail.com',
    description='Leancloud SMS Service for Flask',
    long_description=__doc__,
    py_modules=['flask_leancloud_sms'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask','requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)