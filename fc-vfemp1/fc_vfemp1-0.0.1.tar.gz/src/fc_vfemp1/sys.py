import os
import fc_simesh

def get_geodirs(dim,d):
  s=get_pathname(dim,d)
  assert s is not None,"Unable to find geo directory for dim=%d and d=%d"%(dim,d)
  fullname=os.path.dirname(os.path.abspath(__file__))
  loc_dir=fullname+os.sep+'geodir'+os.sep+s
  from fc_simesh import sys as fsys
  simesh_dir=fsys.get_geodirs(dim,d)
  simesh_dir.insert(0,loc_dir)
  return simesh_dir
  
def get_pathname(dim,d):
  if dim==2 and d==2:
    return '2d'
  if dim==3 and d==2:
    return '3ds'
  if dim==3 and d==3:
    return '3d'
  return None

# geofile without path and without ext
def get_geo(dim,d,geofile):
  (geodir,geofile)=os.path.split(geofile)
  #assert geodir=='', "geofile must be without path: %s"%(geofile)
  (geofile,geoext)=os.path.splitext(geofile)
  assert geoext=='.geo' or geoext=='', "Extension must be .geo in %s"%geofile
  if geodir!='':
    fullgeo=geodir+os.sep+geofile+'.geo'
    if os.path.isfile(fullgeo):
      return (geodir,geofile)
    print('geofile %s.geo not found in directory %s'%(geofile,geodir))
    print('Trying default directories ...')
  geodirs=get_geodirs(dim,d)
  for di in geodirs:
    fullgeo=di+os.sep+geofile+'.geo'
    if os.path.isfile(fullgeo):
      return (di,geofile)
  assert False,"geofile %s.geo not found!"%geofile