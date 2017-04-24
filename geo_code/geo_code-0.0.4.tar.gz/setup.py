from setuptools import setup

setup(name='geo_code',
      version='0.0.4',
      description='Lightweight Python module for geocoding addresses via the Google Geocoding API',
      url='https://github.com/jwilber/geo_code',
      author='Jared Wilber',
      author_email='jdwlbr@gmail.com',
      license='GNU3',
      packages=['geo_code'],
      install_requires=[
            'pandas',
            'requests',
      ],
      zip_safe=False)
