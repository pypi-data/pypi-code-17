#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Command

EXCLUDE_FROM_PACKAGES = []

setup(
	name = 'adbgui',
	version = '0.1',
	description = 'An adb Gui tool',
	author = 'zhangfeng.zou',
	author_email = 'jeff.chau@hotmail.com',
	url = 'http://www.en7788.com',
	license="MIT",
        keywords = 'adb GUI Python',	
	package_dir = {
		'FormUI' : 'FormUI',
		'.':'.'
	},
	packages=["FormUI","."],
    	include_package_data=True,
	package_data = {
	   '.':['./*.xml'],
	},
	entry_points={
        'console_scripts': [
            # allow user to type gdbgui from terminal to automatically launch the server and a tab in a browser
            'adbgui = adbgui.adbgui'
        ],
    	},
	zip_safe=False,
	install_requires=['wxpython'],
)
