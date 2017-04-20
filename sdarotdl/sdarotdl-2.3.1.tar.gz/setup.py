# to register and upload to pypi:
#   python setup.py sdist bdist_wheel
#   twine upload dist/sdarotdl-2.3.0.tar.gz dist/sdarotdl-2.3.0-py2-none-any.whl

from setuptools import setup

from sdarotdl import VERSION_NUMBER

requirements = []
with open('requirements.txt') as f:
    l = f.readline()
    while l:
        req = l.strip()
        l = f.readline()

        if len(req)==0:
            continue

        requirements.append(req)

setup(
    name='sdarotdl',
    version=VERSION_NUMBER,
    # author='',
    # author_email='',
    # maintainer='',
    # maintainer_email='',
    # url='',
    description='Download videos from sdarot.pm website',
    # long_description='',
    # download_url='',
    # classifiers=[],
    # platforms=[],
    # license='',

    install_requires = requirements,

    # packages=[],
    py_modules = ['sdarotdl'],
    entry_points = {
        'console_scripts': [
            'sdarotdl = sdarotdl:main'
            ],
        }
    )
