from setuptools import setup

setup(name='ivs-calculator',
      version='1.1',
      description='Calculator for IVS project.',
      url='https://github.com/NoName115/IVS',
      author='xbazik00, xkolcu00, xcubae00, xkurak00',
      author_email='martin.bazik@gmail.com',
      license='GPL3',
      packages=['src'],
      zip_safe=False,
      install_requires=['PyQt5', 'numpy','wheel'],
      include_package_data=True,
      scripts=['src/ivs-calculator']
)
