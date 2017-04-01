from setuptools import setup, find_packages

DESCRIPTION = (
    '''
    implementation of simple paths algorithm
    '''
)

setup(
    name='simple_paths_algorithm',
    version='0.0.8',
    description=DESCRIPTION,
    url='https://github.com/andrew-lee2/simple_paths_algorithm',
    author='Andrew Lee, Douglas Shier',
    author_email='leeandrew2@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'pandas',
        'networkx',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
