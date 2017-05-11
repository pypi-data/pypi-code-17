'''
 @package   pysolvertools
 @file      setup.py
 @brief     Install pysolvertools
 @copyright GPLv3
 @author    Loic Hausammann <loic_hausammann@hotmail.com>
 @section   COPYRIGHT  Copyright (C) 2017 EPFL (Ecole Polytechnique Federale de Lausanne)  LASTRO - Laboratory of Astrophysics of EPFL

'''

import sys,os,string,glob

from distutils.sysconfig import *
from distutils.core import setup,Extension
from distutils.command.build_ext import build_ext
from distutils.command.install import install
from distutils.command.install_data import install_data

import numpy

INCDIRS=['src']
INCDIRS.append(numpy.get_include())

SRC = glob.glob('src/*.c')


######################
# extensions  

ext_modules = []

ext_modules.append(Extension("pysolvertools._pysolvertools", SRC, include_dirs=INCDIRS))

######################
# list of packages


packages = [
  'pysolvertools',
  ]

setup 	(       name	       	= "pysolvertools",
       		version         = "0.1",
       		author	      	= "Loic Hausammann",
       		author_email    = "loic_hausammann@hotmail.com",
		url 		= "https://gitlab.com/loikki/pySolverTools",
       		description     = "Fast python PDE equation solver.",
		
		packages 	= packages,
		keywords        = ["Solver", "PDE", "Poisson"],

                ext_modules 	= ext_modules,

		#data_files      = data_files,
			    
                #scripts = SCRIPTS			    
 	)
		
