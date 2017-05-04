from setuptools import setup, find_packages
 
setup(
    name='ODTReader',
    packages = ['ODTReader'],
    version='0.0.4',
    url='https://github.com/KaneGalba/ODTReader/',
    download_url='https://github.com/KaneGalba/ODTReader/archive/master.zip',
    author='Kane Galba',
    author_email='kane@galba.co',
    description='Lightweight python module to allow extracting text from OpenDocument (odt) files.',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='GPL',
    install_requires=[],
)
