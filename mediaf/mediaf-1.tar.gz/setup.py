from setuptools import setup
import os
os.system("sudo apt-get install libmp3lame-dev")
os.system("sudo apt-get install ffmpeg")
setup(
name='mediaf',
py_modules=['mediaf'],
version='1',
description='pip install mediaf',
url='https://github.com/RashadGarayev/mediaf',
author='Rashad Garayev',
author_email='pythonaz@yahoo.com',
classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    
],
license='MIT',
keywords='mediaf',
)
