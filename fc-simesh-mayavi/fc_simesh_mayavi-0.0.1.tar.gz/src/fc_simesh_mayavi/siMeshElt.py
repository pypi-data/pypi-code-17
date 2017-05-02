from tvtk.api import tvtk
from mayavi import mlab
import numpy as np

from fc_tools.others import LabelBaseName
from fc_tools.colors import check_color
from fc_tools.graphics import Plane
from fc_simesh.siMeshElt import issiMeshElt,move_mesh,mesh_label,getLocalValue
import fc_mayavi4mesh.simplicial as mlab4sim

#def mesh_label(sTh):
  #assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  #return 'd=%d, lab=%d'%(sTh.d,sTh.label)

def plotmesh(sTh,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  kwargs['name']=kwargs.get('name', mesh_label(sTh) )
  kwargs['color']=check_color(kwargs.pop('color', sTh.color))
  return mlab4sim.plotmesh(sTh.q,sTh.me,**kwargs)

def plot(sTh,u,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  return mlab4sim.plot(sTh.q,sTh.me,getLocalValue(sTh,u),**kwargs)

def plotiso(sTh,u,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert sTh.d==2
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  return mlab4sim.plotiso(sTh.q,sTh.me,getLocalValue(sTh,u),**kwargs)

def iso_surface(sTh,u,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert sTh.dim==3 and sTh.d==3
  return eval("iso_surface_SubTh"+str(sTh.d)+"simp"+str(sTh.dim)+"D(sTh,u,**kwargs)")

def slicemesh(sTh,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert(sTh.dim==3 and sTh.d==3)
  return mlab4sim.slicemesh(sTh.q,sTh.me,**kwargs)

def slice(sTh,u,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert(sTh.dim==3 and sTh.d==3)
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  return mlab4sim.slice(sTh.q,sTh.me,getLocalValue(sTh,u),**kwargs)

def sliceiso(sTh,u,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert(sTh.dim==3 and sTh.d==3)
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  return mlab4sim.sliceiso(sTh.q,sTh.me,getLocalValue(sTh,u),**kwargs)

  
# V a numpy array dim-by-nq
def quiver(sTh,V,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert(sTh.d>=2)
  assert(sTh.dim == V.shape[0])
  return eval("quiver_SubTh"+str(sTh.d)+"simp"+str(sTh.dim)+"D(sTh,V,**kwargs)")

# V a numpy array dim-by-nq
def streamline(sTh,u,V,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  assert( (sTh.d==3) and (sTh.dim==3) )
  assert(sTh.dim == V.shape[0])
  return eval("streamline_SubTh"+str(sTh.d)+"simp"+str(sTh.dim)+"D(sTh,u,V,**kwargs)")

def PlotElementsNumber(sTh,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  Ba=sTh.barycenters()
  if sTh.dim==2:
    for k in range(sTh.nme):
      mlab.text(Ba[k,0],Ba[k,1],str(k),z=0)
  if sTh.dim==3:
    for k in range(sTh.nme):
      mlab.text(Ba[k,0],Ba[k,1],str(k),z=Ba[k,2])              
            
def PlotGradBaCo(sTh,**kwargs):
  assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  scale=kwargs.get('scale', 10)
  Ba=sTh.Barycenters()
  Normal=sTh.NormalFaces()
  Colors=selectColors(sTh.d+1)

  if sTh.dim==2:
    for i in range(sTh.d+1):
      plt.quiver(Ba[0],Ba[1],Normal[i,0,:],Normal[i,1,:],units='x',color=Colors[i],scale=scale)
      
      xlist = []
      ylist = [] 
      for k in range(sTh.nme):
        xlist.extend((Ba[0,k],sTh.q[sTh.me[i,k],0]))
        xlist.append(None)
        ylist.extend((Ba[1,k],sTh.q[sTh.me[i,k],1]))
        ylist.append(None)
      plt.plot(xlist,ylist,color=Colors[i],ls=':') 
  elif sTh.dim==3:
    for i in range(sTh.d+1):
      plt.quiver(Ba[0],Ba[1],Ba[2],Normal[i,0,:],Normal[i,1,:],Normal[i,2,:],units='x',color=Colors[i],scale=scale)
      
      xlist = [];ylist = [];zlist =[]
      for k in range(sTh.nme):
        xlist.extend((Ba[0,k],sTh.q[sTh.me[i,k],0]))
        xlist.append(None)
        ylist.extend((Ba[1,k],sTh.q[sTh.me[i,k],1]))
        ylist.append(None)
        zlist.extend((Ba[2,k],sTh.q[sTh.me[i,k],2]))
        zlist.append(None)
      plt.plot3(xlist,ylist,zlist,color=Colors[i],ls=':')
