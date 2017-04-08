from distutils.core import setup

setup(
    name='pydobot',
    packages=['pydobot'],
    version='0.9.21',
    description='Python 3 library for Dobot Magician',
    author='Luis Mesas',
    author_email='luismesas@gmail.com',
    url='https://github.com/luismesas/pydobot',
    download_url='https://github.com/luismesas/pydobot/archive/0.9.21.tar.gz',
    keywords=['dobot', 'magician', 'robotics'],
    classifiers=[],
    install_requires=[
        'pyserial'
    ]
)
