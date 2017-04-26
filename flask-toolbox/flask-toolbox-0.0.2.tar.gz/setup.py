from setuptools import setup

setup(
    name='flask-toolbox',
    version='0.0.2',
    description='A flask toolbox.',
    author='TuuZed',
    author_email='liuyonghui.job@gmail.com',
    url='https://github.com/TuuZed/flask_toolbox',
    license='Apache License 2.0',
    package_dir={'flask_toolbox': ''},
    packages=['flask_toolbox'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask>=0.8',
    ],
)
