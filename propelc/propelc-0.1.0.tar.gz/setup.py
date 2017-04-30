from setuptools import setup, find_packages

setup(
    name="propelc",
    version="0.1.0",
    author="Mardix",
    py_modules=['propelc'],
    entry_points=dict(console_scripts=[
        'propelc=propelc:cmd',
    ]),
    include_package_data=True,
    install_requires=[
        "ansible>=2.2",
        "sh==1.11",
        "boto==2.39.0",
        "tld==0.7.2",
        "pyyaml>=3.11"
    ],
    zip_safe=False
)

