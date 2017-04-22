# coding=utf-8
import io

from setuptools import setup

try:
    from pypandoc import convert


    def read_md(file_name):
        # http://stackoverflow.com/a/23265673/752142
        return convert(file_name, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")


    def read_md(file_name):
        try:
            return io.open(file_name, 'r', encoding='utf-8').read()
        except UnicodeDecodeError:
            return "Encoding problems with README.md"

# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
setup(
    name='django_cbtp_email',
    version='0.1.0',
    description='TODO Add description',

    # ########################################################################
    #
    # README.rst is generated from README.md:
    #
    # $ pandoc --from=markdown --to=rst README.md -o .tmp/README.rst
    #
    # ~ OR ~
    #
    # $ fab build
    # ########################################################################
    long_description=read_md('README.md'),

    url='https://github.com/illagrenan/django-cbtp-email',
    license='MIT',
    author='Vašek Dohnal',
    author_email='vaclav.dohnal@gmail.com',

    # The exclude makes sure that a top-level tests package doesn’t get
    # installed (it’s still part of the source distribution)
    # since that would wreak havoc.
    # find_packages(exclude=['tests*'])
    packages=['django_cbtp_email'],

    install_requires=['django', 'premailer', 'django-annoying'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
)
