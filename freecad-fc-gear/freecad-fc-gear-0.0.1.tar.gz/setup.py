from setuptools import setup
from freecad.modules.fc_gear import __version__
# name: this is the name pip is using.
# Packages using the same name here cannot be installed together

setup(name='freecad-fc-gear',
      version=__version__,
      packages=['freecad',
                'freecad.modules',
                'freecad.modules.fc_gear',
                'freecad.modules.fc_gear.gearfunc'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/FCGear",
      description="Gear-workbench for freecad",
      install_requires=['numpy'],
      include_package_data=True)
