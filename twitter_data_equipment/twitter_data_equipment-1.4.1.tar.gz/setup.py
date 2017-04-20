from setuptools import setup

setup(name='twitter_data_equipment',
      version='1.4.1',
      description='A package to cluster tools for harvesting, hydrating, cleaning and visualize twitter data',
      url='https://github.com/HolzmanoLagrene/FacharbeitLenzBaumannHS16FS17',
      author='Lenz Baumann',
      author_email='lnzbmnn@gmail.com',
      license='MIT',
      packages=['twitter_data_equipment','twitter_data_equipment.data_sheets'],
      install_requires=[
          'matplotlib'
      ],
      zip_safe=False)

