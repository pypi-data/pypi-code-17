from setuptools import setup, find_packages

setup_defaults = {  
   'name'        : 'fc_simesh_matplotlib',
   'description' : 'Matplotlib add-on to the fc_simesh package',
   'version'     : '0.0.1',
   'url'         : 'http://www.math.univ-paris13.fr/~cuvelier/software',
   'author'      : 'Francois Cuvelier',
   'author_email': 'cuvelier@math.univ-paris13.fr',
   'license'     : 'BSD',
   'packages'    : ['fc_simesh_matplotlib'],
   'classifiers':['Topic :: Scientific/Engineering'],
   } 

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
      install_requires=['fc_simesh >= 0.0.3','fc_matplotlib4mesh >= 0.0.3'],
     )