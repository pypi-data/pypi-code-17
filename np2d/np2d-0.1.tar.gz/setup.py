# Try using setuptools first, if it's installed
try:
    from setuptools import setup
except:
    from distutils.core import setup

# define all packages for distribution
packages = [
    'np2d',
    'np2d.tests'
]

setup(name='np2d',
      version='0.1',
      description='Common 2-D NumPy operations.',
      author='Zach Sailer',
      author_email='zachsailer@gmail.com',
      url='https://github.com/Zsailer/np2d',
      license="MIT",
      packages=packages,
      keywords=["numpy", "2d", "arrays"],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
      ],
      zip_safe=False)
