from setuptools import setup, find_packages

setup_defaults = {  
   'name'        : 'fc_vfemp1',
   'description' : 'Solve scalar and vector Boundary Value Problems by P1-Lagrange ﬁnite element method in any space dimension',
   'version'     : '0.0.1',
   'url'         : 'http://www.math.univ-paris13.fr/~cuvelier/software',
   'author'      : 'Francois Cuvelier',
   'author_email': 'cuvelier@math.univ-paris13.fr',
   'license'     : 'BSD',
   'packages'    : ['fc_vfemp1'],
   'classifiers':['Topic :: Scientific/Engineering'],
   } 

import glob
geofiles=glob.glob("src/fc_oogmsh/geodir/2d/*.geo")+glob.glob("src/fc_oogmsh/geodir/3d/*.geo")+glob.glob("src/fc_oogmsh/geodir/3ds/*.geo")

setup(name=setup_defaults['name'],
      description = setup_defaults['description'],
      version=setup_defaults['version'],
      url=setup_defaults['url'],
      author=setup_defaults['author'],
      author_email=setup_defaults['author_email'],
      license = setup_defaults['license'],
      platforms=["Linux"],#, "Mac OS-X", 'Windows'],
      #packages=setup_defaults['packages'],
      packages=find_packages('src'),  # include all packages under src
      package_dir={'':'src'},   # tell distutils packages are under src
      classifiers=setup_defaults['classifiers'],
      install_requires=['fc_simesh >= 0.0.5'],
      package_data={
        'fc_vfemp1': ['geodir/2d/*.geo','geodir/3d/*.geo','geodir/3ds/*.geo'],
      },
      extras_require={
        'mayavi':  ["fc_simesh_mayavi"],
        'matplotlib': ["fc_simesh_matplotlib"],
      }
     )