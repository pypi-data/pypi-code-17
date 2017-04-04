from setuptools import setup
 
setup(
	name='DroneDataConversion',
	packages = ['DroneDataConversion'],
	version='0.4',
	description = 'Parses Bebop Drones flight logs for further processing and analysis',
	author = 'Johannes Kinzig',
	author_email = 'johannes_kinzig@icloud.com',
	url = 'https://johanneskinzig.de/software-development/python-parser-bebop-logs.html',
	include_package_data=True,
	license='Apache License, Version 2.0',
	install_requires=[
        "geopy",
        "gpxpy",
    ]
	)
