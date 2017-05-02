#import matplotlib.pyplot as plt
#from matplotlib.patches import Patch
import  numpy as np
from tvtk.api import tvtk
from mayavi import mlab
from fc_tools.others import LabelBaseName
from fc_tools.colors import check_color
from fc_tools.mayavi import fc_legend
from fc_simesh.siMesh import issiMesh
import fc_mayavi4mesh.simplicial as mlab4sim 

from . import siMeshElt as sME

def plotmesh(Th,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.pop('d',Th.d)
  labels=kwargs.pop('labels',Th.sThlab[Th.find(d)])
  legend=kwargs.pop('legend',False)
  merge=kwargs.pop('merge',False)
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    name='plotmesh: d=%d, %s'%(d,str(labels))
    return mlab4sim.plotmesh(q,me,name=name,**kwargs)
  if isinstance(labels,int):
    labels=[labels]
  #move=kwargs.pop('move',None)
  handles=[];names=[];colors=[];
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.plotmesh(Th.sTh[k],**kwargs)
      handles.append(h)
      colors.append(Th.sTh[k].color)
      names.append('d=%d,lab=%d'%(d,Th.sTh[k].label))
  if legend:
    fc_legend(names,colors,d)
  return handles 
        
def plot(Th,u,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.pop('d', Th.d)
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  kwargs['colormap']=kwargs.get('colormap','viridis')
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  merge=kwargs.pop('merge',True)
  name=kwargs.pop('name', None)
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='plot: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.plot(q,me,u[toGlobal],**kwargs)
  
  if isinstance(labels,int):
    labels=[labels]
  handles=[]
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      if name is None:
        Name='plot: d=%d, label=%s'%(d,str(l))
      else:
        Name=name
      h=sME.plot(Th.sTh[k],u,name=Name,**kwargs)
      handles.append(h)
  return handles
      
def iso_surface(Th,u,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.pop('d', Th.d)
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  kwargs['colormap']=kwargs.get('colormap','viridis')
  contours=kwargs.pop('contours', 10)
  merge=kwargs.pop('merge',True)
  name=kwargs.pop('name', None)
  if isinstance(contours,int):
    kwargs['contours']=list(np.linspace(min(u),max(u),contours))
    
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='iso_surface: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.iso_surface(q,me,u[toGlobal],**kwargs)
  
  handles=[]
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.iso_surface(Th.sTh[k],u,**kwargs)
      handles.append(h)
  return handles

#def scalar_cut_plane(Th,u,**kwargs):
def slice(Th,u,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  assert Th.dim==3 and Th.d==3 
  d=3
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  kwargs['colormap']=kwargs.get('colormap','viridis')
  merge=kwargs.pop('merge',True)
  name=kwargs.pop('name', None)
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='slice: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.slice(q,me,u[toGlobal],**kwargs)
  handles=[]
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.slice(Th.sTh[k],u,**kwargs)
      handles.append(h)
  return handles
      
def sliceiso(Th,u,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  assert Th.dim==3 and Th.d==3 
  d=3
  kwargs['colormap']=kwargs.get('colormap','viridis')
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  contours=kwargs.pop('contours', 10)
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));
  merge=kwargs.pop('merge',True)
  name=kwargs.pop('name', None)
  if vmax-vmin<1e-14:
    return
  kwargs['vmax']=vmax
  if isinstance(contours,int):
    kwargs['contours']=list(np.linspace(min(u),max(u),contours))
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='sliceiso: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.sliceiso(q,me,u[toGlobal],**kwargs)  
  handles=[]  
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.sliceiso(Th.sTh[k],u,**kwargs)
      handles.append(h)
  return handles

def slicemesh(Th,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  assert Th.dim==3 and Th.d==3 
  d=3
  name=kwargs.pop('name', None)
  merge=kwargs.pop('merge', True)
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='slicemesh: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.slicemesh(q,me,**kwargs)
  handles=[] 
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.slicemesh(Th.sTh[k],**kwargs)
      handles.append(h)
  return handles
      
def plotiso(Th,u,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.pop('d', 2)
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  contours=kwargs.pop('contours', 10)
  kwargs['colormap']=kwargs.get('colormap','viridis')
  name=kwargs.pop('name', None)
  merge=kwargs.pop('merge', True)
  if isinstance(contours,int):
    kwargs['contours']=list(np.linspace(min(u),max(u),contours))
  else:
    kwargs['contours']=list(contours)
  if merge:
    (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
    if name is None:
      kwargs['name']='plotiso: d=%d, labels=%s'%(d,str(labels))
    return mlab4sim.plotiso(q,me,u[toGlobal],**kwargs)
  handles=[] 
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      h=sME.plotiso(Th.sTh[k],u,**kwargs)
      handles.append(h)
  return handles
  
    
def quiver(Th,V,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.pop('d', Th.d)
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  scalars=kwargs.get('scalars', None )
  name=kwargs.pop('name', None)
  color=kwargs.pop('color', None)
  kwargs['colormap']=kwargs.get('colormap','viridis')
  if color is not None:
    kwargs['color']=check_color(color)
  if scalars is None:
    Norm=np.sqrt(np.sum(V**2,axis=0))
    vmin=min(Norm);vmax=max(Norm)
  else:
    vmin=min(scalars);vmax=max(scalars)
  vmin=kwargs.pop('vmin',vmin)
  kwargs['vmin']=vmin
  vmax=kwargs.pop('vmax',vmax)
  kwargs['vmax']=vmax
  if name is None:
    kwargs['name']='quiver: d=%d, labels=%s'%(d,str(labels))
  (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
  N=len(toGlobal)
  W=np.zeros((Th.dim,N))
  for i in np.arange(Th.dim):
    W[i]=V[i][toGlobal]
    
  if scalars is not None:
      kwargs['scalars']=scalars[toGlobal]
  return mlab4sim.quiver(q,me,W,**kwargs)    
  

def streamline(Th,u,V,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  assert( Th.dim==3 and Th.d==3 )
  d=Th.d
  labels=kwargs.pop('labels', Th.sThlab[Th.find(d)])
  scalars_name=kwargs.pop('scalars_name', 'scalars')
  vectors_name=kwargs.pop('vectors_name', 'vectors')
  kwargs['colormap']=kwargs.get('colormap','viridis')
  name=kwargs.pop('name', None)
  kwargs['vmin']=kwargs.pop('vmin',min(u))
  kwargs['vmax']=kwargs.pop('vmax',max(u))
  if name is None:
    kwargs['name']='streamline: labels=%s'%(str(labels))
  (q,me,toGlobal)=Th.get_mesh(d=d,labels=labels)
  N=len(toGlobal)
  W=np.zeros((Th.dim,N))
  for i in np.arange(Th.dim):
    W[i]=V[i][toGlobal]
  U=u[toGlobal]
  return mlab4sim.streamline(q,me,U,W,**kwargs)
 
def vtkPlotGradBaCo(Th,**kwargs):
  assert issiMesh(Th), "First argument must be a siMesh object"
  d=kwargs.get('d', Th.d)
  labels=kwargs.get('labels', Th.sThlab[Th.find(d)])
  #PlotOptions=kwargs.get('PlotOptions', {})
  for l in labels:
    k=Th.find(d,labels=l)
    if k is not None:
      sME.vtkPlotGradBaCo(Th.sTh[k])
