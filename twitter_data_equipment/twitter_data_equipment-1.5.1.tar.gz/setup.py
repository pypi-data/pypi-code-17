from setuptools import setup

setup(name='twitter_data_equipment',
      version='1.5.1',
      description='A package that wraps tools for harvesting, hydrating, cleaning and visualize twitter data',
      url='https://github.com/HolzmanoLagrene/FacharbeitLenzBaumannHS16FS17',
      author='Lenz Baumann',
      author_email='lnzbmnn@gmail.com',
      license='MIT',
      packages=['twitter_data_equipment'],
      install_requires=['bs4', 'pandas', 'numpy', 'python-louvain', 'matplotlib', 'networkx', 'twarc'],
      include_package_data=True,
      zip_safe=False)

