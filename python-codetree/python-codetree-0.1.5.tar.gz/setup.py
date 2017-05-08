from setuptools import setup, find_packages

setup(
    name="python-codetree",
    version="0.1.5",
    description="A code tree builder",
    url="https://launchpad.net/codetree",
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers"],
    entry_points={
        "console_scripts": ['codetree = codetree.cli:main']},
    include_package_data=False,
    install_requires=['futures', 'requests', 'six']
)
