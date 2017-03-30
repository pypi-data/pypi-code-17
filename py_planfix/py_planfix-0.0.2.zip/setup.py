from distutils.core import setup

setup(
    name='py_planfix',
    version='0.0.2',
    packages=['py_planfix'],
    url='https://github.com/zloiia/py_planfix',
    license='MIT',
    author='zloiia',
    author_email='zloiiaarhpgu@gmail.com',
    description='',
    install_requires= [
        'requests',
        'schema',
        'dicttoxml',
        'xmltodict>=0.10.2'
    ],
)
