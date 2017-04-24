import os
import setuptools
import sys

with open("yaz_templating_plugin/version.py") as file:
    globals = {}
    exec(file.read(), globals)
    version = globals["__version__"]

if sys.argv[-1] == "tag":
    os.system("git tag -a {} -m \"Release {}\"".format(version, version))
    os.system("git push origin {}".format(version))
    sys.exit()

if sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist upload")
    os.system("python3 setup.py bdist_wheel upload")
    sys.exit()

setuptools.setup(
    name='yaz_templating_plugin',
    packages=['yaz_templating_plugin'],
    version=version,
    description='A templating plugin for YAZ',
    author='Boudewijn Schoon',
    author_email='yaz@frayja.com',
    url="https://github.com/yaz/yaz_templating_plugin",
    install_requires=['yaz', 'jinja2', 'colored'],
    license='MIT',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ])
