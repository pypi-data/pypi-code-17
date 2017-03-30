from setuptools import setup, find_packages

setup(
    name = 'PyPokerGUI',
    version = '0.0.1',
    author = 'ishikota',
    author_email = 'ishikota086@gmail.com',
    description = 'GUI application for PyPokerEngine',
    license = 'MIT',
    keywords = 'python poker engine gui',
    url = 'https://github.com/ishikota/PyPokerGUI',
    packages = [pkg for pkg in find_packages() if pkg != "tests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
    ],
    entry_point={
        'console_scripts': ['pypokergui=pypokergui.__main__:cli']
    },
    )

