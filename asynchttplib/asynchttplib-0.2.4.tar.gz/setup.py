from setuptools import setup, find_packages


setup(
    name='asynchttplib',
    version='0.2.4',
    description='Lib for creating microservice on asyncio',
    author='Oleksii Moisieienko',
    author_email='me@alexmay23.com',
    license='MIT',
    packages=find_packages(exclude=['dist','docs', 'tests']),
    install_requires=['aiohttp', 'aioamqp', 'motor', 'webargs', 'uvloop', 'aioredis', 'flatdict']
)