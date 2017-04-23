from setuptools import setup 
setup ( 
		name='KissDownloader',
		version='1',
		description = 'A kisscartoon/kissanime downloader' ,
		package_dir={'kissdownloader':'C:\\Python34'},
		author='Vriska',
		author_email='anirudhgan@gmail.com',
		install_requires = ['bs4','cfscrape','requests'],
		package_data={'data' : ['C:\Program Files\PhantomJS\phantomjs.exe']},
		)
		