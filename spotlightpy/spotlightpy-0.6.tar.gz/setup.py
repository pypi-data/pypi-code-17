from setuptools import setup


setup(	name = 'spotlightpy',
		version = 0.6,
		description = 'Extract Images from Microsoft Spotlight Project(Windows X only)',
		classifiers = [
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3 :: Only",
		"Operating System :: Microsoft :: Windows",
		],
		keywords = 'spotlight Microsoft Windows10 HDImages',
		url = 'https://github.com/joshikunal94/spotlightpy',
		author = 'Kunal Joshi',
		author_email = 'joshikunal16@gmail.com',
		license = 'MIT',
		packages = ['spotlightpy'],
		install_requires = [
							'pillow',
							],
		include_package_data = True,
		zip_safe = False	)