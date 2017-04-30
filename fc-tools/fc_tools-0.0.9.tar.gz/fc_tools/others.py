def isModuleFound(name,**kwargs):
  verbose=kwargs.get('verbose',False)
  isOk=True
  try:
    __import__(name)
  except ImportError:
    isOk=False
    if verbose:
      print('%s is not founded!'%name)
  return isOk

def LabelBaseName(dim,d):
  if (d==dim):
    return r"\Omega"
  if (d+1==dim):
    return r"\Gamma"
  if (d+2==dim):
    return r"\partial\Gamma"
  if (d+3==dim):
    return r"\partial^2\Gamma"
    
    
def LabelBaseNameSimp(dim,d,ds):
  if (d==dim):
    return LabelBaseName(dim,ds)
  if (d+1==dim):
    return LabelBaseName(dim,ds+1)
  if (d+2==dim):
    return LabelBaseName(dim,ds+2)
  if (d+3==dim):
    return LabelBaseName(dim,ds+3)
  
def print_packages(packages):
  #packages=['fc_tools','fc_hypermesh','fc_oogmsh','fc_simesh','fc_matplotlib4mesh']
  for name in packages:
    print('package %s:'%name)
    if isModuleFound(name):
      f=__import__(name)
      print('  path    : %s'%f.__path__[0])
      print('  version : %s'%f.__version__)
    else:
      print('  not found')