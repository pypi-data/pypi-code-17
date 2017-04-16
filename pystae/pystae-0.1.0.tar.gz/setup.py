from distutils.core import setup

setup(
    name="pystae",
    author="vin tang",
    author_email="vin.tang@gmail.com",
    version="0.1.0",
    packages=["pystae"], # source code folder
    url='https://github.com/mynameisvinn/pystae',

    # Dependent packages (distributions)
    install_requires=[
        "pandas", "requests"
    ],
)
