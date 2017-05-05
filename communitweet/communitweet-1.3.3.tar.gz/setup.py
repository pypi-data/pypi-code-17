from setuptools import setup

setup(name='communitweet',
      version='1.3.3',
      description='A package that wraps tools for harvesting, hydrating, cleaning and visualize twitter data',
      url='https://github.com/HolzmanoLagrene/FacharbeitLenzBaumannHS16FS17',
      author='Lenz Baumann',
      author_email='lnzbmnn@gmail.com',
      license='MIT',
      packages=['communitweet'],
      install_requires=['bs4 >= 0.0.1',
                        'pandas >= 0.19.2',
                        'numpy >= 1.12.1',
                        'python-louvain >= 0.6',
                        'matplotlib >= 2.0.1',
                        'networkx >= 1.11 ',
                        'twarc >= 1.1.1'],
      include_package_data=True,
      zip_safe=False)

