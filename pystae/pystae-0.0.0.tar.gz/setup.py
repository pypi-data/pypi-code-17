from setuptools import setup

setup(
    author="vin tang",
    author_email="vin.tang@gmail.com",
    url="https://github.com/mynameisvinn/pystae",
    name="pystae",
    packages=["pystae"],
    install_requires=["pandas", "requests", "joblib"],
    test_suite='tests'
)
