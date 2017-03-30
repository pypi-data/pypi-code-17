from setuptools import setup


setup(
    name='django-datetimepicker',
    packages=['datetimepicker',],
    package_data={'datetimepicker': ['static/datetimepicker/css/*.css',
                                     'static/datetimepicker/js/*.js',
                                     'static/datetimepicker/vendor/js/jquery.min.js']},
    include_package_data=True,
    version='2.3.1',
    description='Datetimepicker for Django projects.',
    long_description=open('README.rst').read(),
    author='Pablo Escodebar',
    author_email='escodebar@gmail.com',
    url='https://github.com/escodebar/django-datetimepicker.git',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
