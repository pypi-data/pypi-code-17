import  os, errno, sys
from fc_tools.others import print_packages
global fcPause

def PrintCopyright():
  print('---------------------------------------------------------------')
  print('Solving Boundary Value Problems (BVP\'s) with fc_vfemp1 package')
  print('Copyright (C) 2017 Cuvelier F.')
  print('  (LAGA/CNRS/University of Paris XIII)')
  print('---------------------------------------------------------------\n')

def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
  
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
      
def pause(message):
  if not run_from_ipython():
    if sys.version_info[0]==3 :
      input(message)
    else:
      raw_input(message)

def print_vfemp1_packages():
  packages=['fc_tools','fc_hypermesh','fc_oogmsh','fc_simesh','fc_matplotlib4mesh','fc_simesh_matplotlib','fc_mayavi4mesh','fc_simesh_mayavi']
  print_packages(packages)