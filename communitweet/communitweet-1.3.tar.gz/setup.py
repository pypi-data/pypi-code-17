from setuptools import setup

setup(name='communitweet',
      version='1.3',
      description='A package that wraps tools for harvesting, hydrating, cleaning and visualize twitter data',
      url='https://github.com/HolzmanoLagrene/FacharbeitLenzBaumannHS16FS17',
      author='Lenz Baumann',
      author_email='lnzbmnn@gmail.com',
      license='MIT',
      packages=['communitweet'],
      install_requires=['bs4', 'pandas', 'numpy', 'python-louvain', 'matplotlib', 'networkx', 'twarc'],
      include_package_data=True,
      zip_safe=False)

