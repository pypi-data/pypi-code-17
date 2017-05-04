from distutils.core import setup

setup(
    name='newbar-afisha',
    version='0.0.2',
    packages=['newbar_afisha'],
    url='https://github.com/strizhechenko/newbar-afisha',
    license='GPL',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    description='CLI util for quick-look for recent events in New Bar (ekb)',
    scripts='scripts/newbar-afisha',
    install_requires=['requests', 'beautifulsoup4']
)
