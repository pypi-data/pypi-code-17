from setuptools import setup, find_packages


setup(
    name='cl_utils',
    version=__import__('cl_utils').__version__,
    url='https://github.com/vikingco/cl_utils',
    license='BSD',
    description='A collection of small utilities',
    long_description=open('README', 'r').read(),
    author='Unleashed NV',
    author_email='operations@unleashed.be',
    packages=find_packages('.'),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
