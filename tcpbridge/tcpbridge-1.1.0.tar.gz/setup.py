from setuptools import setup

setup(
    name="tcpbridge",
    version="1.1.0",
    author="Denis Chagin",
    author_email="denis.chagin@emlid.com",
    url="https://github.com/emlid/tcp-bridge",
    packages=["tcpbridge"],
    extras_require={
        'test': ['pytest', 'pytest-cov'],
    }
)
