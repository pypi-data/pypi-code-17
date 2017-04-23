from setuptools import setup ,find_packages
setup ( 
		name='KissDownloader',
		version='2',
		description = 'A kisscartoon/kissanime downloader' ,
		packages=['scr'],
		author='Vriska',
		author_email='anirudhgan@gmail.com',
		install_requires = ['bs4','cfscrape','requests'],
		data_files=[('C:\Program Files\PhantomJS' , ['C:\Program Files\PhantomJS\phantomjs.exe'])],
		)
		