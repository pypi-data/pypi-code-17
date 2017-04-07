from setuptools import setup


version = '0.0.1'

setup(
    name='dmu-utils',
    version=version,
    description='DMU Utils',
    author='Dmitry Mugtasimov',
    author_email='dmugtasimov@gmail.com',
    url='https://github.com/dmugtasimov/dmu-utils',
    packages=['dmu_utils'],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    extras_require={},
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
