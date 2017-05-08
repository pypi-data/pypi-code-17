from distutils.core import setup

setup(
    name='perfecto',
    packages=['perfecto','perfecto/client', 'perfecto/Exceptions', 'perfecto/model', 'perfecto/test'],  # this must be the same as the name above
    version='0.1.1.4',
    description='Perfecto Reporting SDK for Python',
    author='Perfecto',
    author_email='perfecto@perfectomobile.com',
    url='https://github.com/PerfectoCode',  # use the URL to the GitHub repo
    download_url='https://github.com/PerfectoCode',
    keywords=['Perfecto', 'PerfectoMobile', 'Reporting', 'Selenium', 'Appium', 'Automation testing'],
    classifiers=[]
)
