from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='findyourday',
        version='0.2',
        description='Finds the day for a given date',
        long_description=readme(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: Freeware',
            'Programming Language :: Python :: 2.7',
            'Natural Language :: English'
            ],
        keywords ='find the day of the week for a date',
        url='http://github.com/nimnathw/findyourday',
        author='Nimnath Withanachchi',
        author_email='nimnathw@gmail.com',
        license='MIT',
        packages=['findyourday'],
        test_suite='nose.collector',
        tests_require=['nose', 'nose-cover3'],
        entry_points={'console_scripts': ['findyourday_find=findyourday.command_line:main']},
        scripts=['bin/findyourday_find'],
        include_package_data=True,
        zip_safe=False,
        )

