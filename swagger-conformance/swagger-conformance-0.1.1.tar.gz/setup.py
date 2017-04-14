from setuptools import find_packages, setup
import pypandoc
import subprocess

URL = 'https://github.com/olipratt/swagger-conformance'
VERSION = '0.1.1'
LONG_DESC = pypandoc.convert('readme.md', 'rst').replace('\r\n', '\n')

# LONG_DESC = subprocess.check_output(['pandoc', 'readme.md', '-t', 'rst']).decode('ascii').replace('\r\n', '\n')
# print(repr(LONG_DESC))
# open('README.rst', 'w').write('\n'.join(pypandoc.convert('readme.md', 'rst'))


setup(
    name='swagger-conformance',
    packages=find_packages(exclude=['examples', 'docs', 'tests']),
    install_requires=['hypothesis', 'pyswagger', 'requests'],
    version=VERSION,
    description="Tool for testing whether your API conforms to its swagger "
                "specification",
    long_description=LONG_DESC,
    author='Oli Pratt',
    author_email='olipratt@users.noreply.github.com',
    url=URL,
    download_url='{}/archive/{}.tar.gz'.format(URL, VERSION),
    keywords=['swagger', 'testing', 'OpenAPI', 'hypothesis'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
