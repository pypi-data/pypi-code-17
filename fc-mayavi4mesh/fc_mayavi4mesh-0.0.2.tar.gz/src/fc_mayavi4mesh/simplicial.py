from tvtk.api import tvtk
from mayavi import mlab
import numpy as np

from fc_tools.others import LabelBaseName
from fc_tools.colors import check_color
from fc_tools.graphics import Plane

def simplicial_dimension(q,me):
  """
    

    Parameters
    ----------
    q : mesh vertices, dim-by-nq or nq-by-dim numpy array where
        dim is the space dimension (2 or 3) and nq the number of vertices.
    me: mesh elements connectivity array where elements are d-simplices. 
        me is a (d+1)-by-nme or nme-by-(d+1) numpy array where nme is the number 
        of mesh eleemnts and d is the simplicial dimension:
          d=0: points, 
          d=1: lines, 
          d=2: triangle, 
          d=3: tetrahedron

    Returns
    -------
    q  : The mesh vertices as a nq-by-dim numpy array
    me : The mesh elements connectivity array as nme-by-(d+1) numpy array
    dim: The space dimension
    d  : The simplicial dimension
  """
  assert (q.shape[0] <=3) or (q.shape[1] <=3)
  if q.shape[1] >3 :
    q=q.T
  dim=q.shape[1]
  
  assert (me.shape[0] <=4) or (me.shape[1] <=4)
  if me.shape[1] >4 :
    me=me.T
  d=me.shape[1]-1
  return q,me,dim,d

def plotmesh(q,me,**kwargs):
  """
  mesh plotting
  
  Parameters
  ----------
    q : mesh vertices, dim-by-nq or nq-by-dim numpy array where
        dim is the space dimension (2 or 3) and nq the number of vertices.
    me: mesh elements connectivity array where elements are d-simplices. 
        me is a (d+1)-by-nme or nme-by-(d+1) numpy array where nme is the number 
        of mesh elements and d is the simplicial dimension:
          d=0: points, 
          d=1: lines, 
          d=2: triangle, 
          d=3: tetrahedron
                  
  Returns
  -------
    handles: 
        
  """
  kind=kwargs.pop('kind', 'simplicial')
  kwargs['color']=check_color(kwargs.pop('color', 'Blue'))
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    move=kwargs.pop('move',None)
    Q=move_mesh(q,move)
    return eval("plotmesh_SubTh"+str(d)+"simp"+str(dim)+"D(Q,me,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def plot(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    return eval("plot_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
def plotiso(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert d==2
    return eval("plotiso_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def slicemesh(q,me,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim==3 and d==3
    return eval("slicemesh_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def slice(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim==3 and d==3
    return eval("slice_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def sliceiso(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim==3 and  d==3
    return eval("sliceiso_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def quiver(q,me,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim>=2
    return quiver_simp(q,V,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
def iso_surface(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim==3 and d==3
    return iso_surface_SubTh3simp3D(q,me,u,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'

def streamline(q,me,u,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    q,me,dim,d=simplicial_dimension(q,me)
    assert dim==3 and d==3
    return streamline_SubTh3simp3D(q,me,u,V,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  

def plotmesh_SubTh1simp2D(q,me,**kwargs):
  lighting=kwargs.pop('lighting', False)
  z=kwargs.pop('z',0*q[:,0])
  line_type = tvtk.Line().cell_type
  ug = tvtk.UnstructuredGrid(points=np.array([q[:,0],q[:,1],z]).T)
  ug.set_cells(line_type, me)
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.lighting=lighting
  return sf

def plotmesh_SubTh2simp2D(q,me,**kwargs):
  lighting=kwargs.pop('lighting', False)
  representation=kwargs.pop('representation','wireframe')
  kwargs['representation']=representation  
  z=kwargs.pop('z',0*q[:,0])
  tm1=mlab.triangular_mesh(q[:,0],q[:,1],z,me,**kwargs)
  tm1.actor.property.lighting=lighting
  return tm1
    
def plotmesh_SubTh1simp3D(q,me,**kwargs):
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  #line_type = tvtk.Line().cell_type
  #ug = tvtk.UnstructuredGrid(points=q)
  #ug.set_cells(line_type, ME)
  ug=UnstructuredGrid(q,ME)
  sf=mlab.pipeline.surface(ug,**kwargs)
  #sf.actor.property.color=color # default
  #sf.actor.property.line_width=linewidth # default
  #sf.name='d=%d, lab=%d'%(sTh.d,sTh.label)
  return sf
  
def plotmesh_SubTh2simp3D(q,me,**kwargs):
  representation=kwargs.get('representation', 'wireframe') # or 'points' or 'surface'
  lighting=kwargs.pop('lighting',False)
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  color=kwargs.pop('color',(0,0,1))
  ug=UnstructuredGrid(q,ME)
  #tri_type = tvtk.Triangle().cell_type
  #ug = tvtk.UnstructuredGrid(points=q)
  #ug.set_cells(tri_type, ME)
  edge_visibility=kwargs.pop('edge_visibility',False)
  edge_color=check_color(kwargs.pop('edge_color',(0,0,0)))
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.edge_visibility=edge_visibility
  sf.actor.property.edge_color=edge_color
  sf.actor.property.representation=representation
  sf.actor.property.color=color # default
  sf.actor.property.lighting=lighting
 
  #sf.actor.property.line_width=linewidth # default
  #sf.name='d=%d, lab=%d'%(sTh.d,sTh.label)
  return sf
  #return triangular_mesh(sTh.q[:,0], sTh.q[:,1], sTh.q[:,2], sTh.me.T, color=color)
  

def cutIndex(q,me,cut_planes):
  # cut_planes is a list of fc_simesh.mayavi_tools.Plane objects
  idxme=np.arange(me.shape[0])
  for i in range(len(cut_planes)):
    assert( isinstance(cut_planes[i] , Plane) )
    #idxme=np.intersect1d(idxme,cutIndexPlane(sTh,cut_planes[i]))
    idxme=np.setdiff1d(idxme,cutIndexPlane(q,me,cut_planes[i]))
  return idxme
      
def cutIndexPlane(q,me,P):
  nq=q.shape[0]
  Z=np.dot( q-np.ones((nq,1))*P.origin , P.normal)
  idx=np.where(Z<0)[0]
  R=np.in1d(me[:,0],idx)
  for i in range(1,me.shape[1]):
    R[:]=R & np.in1d(me[:,i],idx) 
  return np.where(~R)[0]

def cutMeshElements(q,me,cut_planes):
  ME=me
  if cut_planes != []:
    idxme=cutIndex(q,me,cut_planes)
    ME=ME[idxme]
  return ME

def plotmesh_SubTh3simp3D(q,me,**kwargs):
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  ug=UnstructuredGrid(q,ME)
  #tet_type = tvtk.Tetra().cell_type
  #ug0 = tvtk.UnstructuredGrid(points=q)
  #ug0.set_cells(tet_type, ME)
  sf=mlab.pipeline.surface(ug,opacity=0.1)
  #sf2=mlab.pipeline.surface(mlab.pipeline.extract_edges(sf), color=color, opacity=opacity )
  sf2=mlab.pipeline.surface(mlab.pipeline.extract_edges(sf), **kwargs )
  #sf2.name='d=%d, lab=%d'%(sTh.d,sTh.label)
  return sf2

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


def plot_SubTh1simp2D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  plane=kwargs.pop('plane', True )
  
  ug=UnstructuredGrid(q,me,scalars=U,scalars_name=name,plane=plane)
  #cmap=kwargs.pop('colormap', 'blue-rscalars_nameed')
  #U=getLocalValue(sTh,u)
  #nq=q.shape[0]
  #if plane:
    #Z=np.zeros((nq,1))
  #else:
    #Z=U.reshape((nq,1))
  #line_type = tvtk.Line().cell_type
  #ug0 = tvtk.UnstructuredGrid(points=np.hstack((q,Z)))
  #ug0.set_cells(line_type, me)
  #ug0.point_data.scalars = U
  #ug0.point_data.scalars.name = name
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf 
  
def plot_SubTh2simp2D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  plane=kwargs.pop('plane', True )
  lighting=kwargs.pop('lighting', False )
  ug=UnstructuredGrid(q,me,scalars=U,scalars_name=name,plane=plane)
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.lighting=lighting
  return sf 
  
def plot_SubTh1simp3D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  #U=getLocalValue(sTh,u)
  ug=UnstructuredGrid(q,me,scalars=U,scalars_name=name)
  #line_type = tvtk.Line().cell_type
  #ug0 = tvtk.UnstructuredGrid(points=q)
  #ug0.set_cells(line_type, me)
  #ug0.point_data.scalars = U
  #ug0.point_data.scalars.name = name
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf 
 
def plot_SubTh2simp3D(q,me,U,**kwargs):
  lighting=kwargs.pop('lighting', False )
  name=kwargs.pop('scalars_name', 'unknown' )
  ug=UnstructuredGrid(q,me,scalars=U,scalars_name=name)
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf

def plot_SubTh3simp3D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  # mlab.pipeline.volume(ug) : BUG
  #  Generic Warning: In VTK-7.0.0/Rendering/Volume/vtkVolumeRayCastMapper.cxx, line 118
  #  vtkVolumeRayCastMapper::vtkVolumeRayCastMapper was deprecated for VTK 7.0 and will be removed in a future version.
  #
  ug=UnstructuredGrid(q,me,scalars=U,scalars_name=name)
  sf=mlab.pipeline.surface(mlab.pipeline.extract_edges(ug),**kwargs)
  return sf
  
def iso_surface_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  N=kwargs.pop('N',10) # number of contours
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  ug=UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf
  
def slice_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  w_enabled=kwargs.pop('w_enabled',False) # Widget enabled
  ug=UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  scp=mlab.pipeline.scalar_cut_plane(ug,**kwargs)
  scp.implicit_plane.widget.enabled = w_enabled
  if normal is not None:
    scp.implicit_plane.plane.normal=normal
  if origin is not None:
    scp.implicit_plane.plane.origin=origin
  return scp
  
def slicemesh_SubTh3simp3D(q,me,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  color=check_color(kwargs.pop('color', (0,0,1)))
  w_enabled=kwargs.pop('w_enabled',False)
  ug=UnstructuredGrid(q,me)
  scp=mlab.pipeline.scalar_cut_plane(ug,color=color,**kwargs)
  scp.implicit_plane.widget.enabled = w_enabled # first : due to BUG with normal
  if normal is not None:
    scp.implicit_plane.plane.normal=normal
  if origin is not None:
    scp.implicit_plane.plane.origin=origin
  return scp
  
def sliceiso_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  w_enabled=kwargs.pop('w_enabled',False)
  color=check_color(kwargs.pop('color', None))
  if color is not None:
    kwargs['color']=color
  ug=UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  cp=mlab.pipeline.cut_plane(ug)
  cp.filters[0].widget.enabled = w_enabled 
  isf=mlab.pipeline.iso_surface(cp,**kwargs)
  if normal is not None:
    cp.filters[0].normal=normal
    cp.filters[0].plane.normal=normal
  if origin is not None:
    cp.filters[0].origin=origin
    cp.filters[0].plane.origin=origin
  return isf
  
def plotiso_SubTh2simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  N=kwargs.pop('N',10) # number of contours
  color=check_color(kwargs.pop('color', None))
  if color is not None:
    kwargs['color']=color
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  ug=UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf 

def plotiso_SubTh2simp2D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  #cmap=kwargs.pop('cmap', 'blue-red')
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  N=kwargs.pop('N',10) # number of contours
  color=kwargs.pop('color', None)
  if color is not None:
    kwargs['color']=check_color(color)
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  plane=kwargs.pop('plane', True )
  ug=UnstructuredGrid(q,me,scalars=u,scalars_name=name,plane=plane)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf
    
#def quiver_SubTh2simp2D(q,me,V,**kwargs):
  #name=kwargs.pop('vectors_name', 'unknown' )
  #ug=UnstructuredGrid(sTh,vectors=V,vectors_name=name)
  #mq=mlab.quiver3d(sTh.q[:,0],sTh.q[:,1],np.zeros((sTh.nq,)),W[0],W[1],np.zeros((sTh.nq,)),**kwargs)
  #if scalars is not None:
    #color_mode=kwargs.pop('color_mode', 'color_by_scalar' )
    #mq.glyph.color_mode=color_mode
  #return mq  

def streamline_SubTh3simp3D(q,me,u,V,**kwargs):
  scalars_name=kwargs.pop('scalars_name', 'scalar data' )
  vectors_name=kwargs.pop('vectors_name', 'vector data' )
  seed_options=kwargs.pop('seed_options', None)
  seed_widget_options=kwargs.pop('seed_widget_options', None)
  streamtracer_options=kwargs.pop('streamtracer_options', None)
  ug=UnstructuredGrid(q,me,scalars=u,vectors=V,scalars_name=scalars_name,vectors_name=vectors_name)
  sf=mlab.pipeline.streamline(ug,**kwargs)
  if seed_options is not None:
    sf.seed.trait_set(**seed_options)
  if streamtracer_options is not None:
    sf.stream_tracer.trait_set(**streamtracer_options)
  if seed_widget_options is not None:
    sf.seed.widget.trait_set(**seed_widget_options)
  e=sf.seed.widget.enabled
  sf.seed.widget.enabled=0
  sf.seed.widget.enabled=1
  sf.seed.widget.enabled=e
  return sf

def quiver_simp(q,V,**kwargs):
  dim=q.shape[1]
  assert dim>=2
  scalars=kwargs.get('scalars', None )
  name=kwargs.pop('name', None)
  color=kwargs.pop('color', None)
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
    kwargs['name']='quiver: dim=%d'%(dim)
  if dim==3:
    z=q[:,2]
    Vz=V[2]
  else:
    z=np.zeros((q.shape[0],))
    Vz=z
  mq=mlab.quiver3d(q[:,0],q[:,1],z,V[0],V[1],Vz,**kwargs)
  if scalars is not None:
    color_mode=kwargs.pop('color_mode', 'color_by_scalar' )
    mq.glyph.color_mode=color_mode
  else: # bug with vmin, vmax in mlab.quiver3d?
    mq.glyph.mask_input_points=True
    mq.module_manager.vector_lut_manager.data_range=np.array([vmin,vmax])
    mq.module_manager.vector_lut_manager.use_default_range=False
  return mq


def iso_surface_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('name', 'unknown' )
  N=kwargs.pop('N',10) # number of contours
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  tet_type = tvtk.Tetra().cell_type
  ug = tvtk.UnstructuredGrid(points=q)
  ug.set_cells(tet_type, me)
  ug.point_data.scalars = u
  ug.point_data.scalars.name = name
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf


#def setLocalScalars(sTh,u):
  #assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  #if len(u)==sTh.nqGlobal:
    #return u[sTh.toGlobal]
  #else:
    #assert( len(u) == sTh.nq )
    #return u

#def setLocalVectors(sTh,V):
  #assert issiMeshElt(sTh), "First argument must be a siMeshElt object"
  #assert(V.shape[0]==sTh.dim)
  #if V.shape[1]==sTh.nqGlobal:
    #return V[:,sTh.toGlobal]
  #else:
    #assert( V.shape[1] == sTh.nq )
    #return V  

# Unstructured grid on siMeshElt
#
#def UnstructuredGrid(sTh,**kwargs):
  #ug=eval("UnstructuredGrid_SubTh"+str(sTh.d)+"simp"+str(sTh.dim)+"D(sTh)")
  #return ug

def UnstructuredGrid(q,me,**kwargs):
  scalars=kwargs.get('scalars', None )
  scalars_name=kwargs.get('scalars_name', 'scalar data' )
  vectors=kwargs.get('vectors', None )
  vectors_name=kwargs.get('vectors_name', 'vector data' )
  plane=kwargs.pop('plane', True )
  q,me,dim,d=simplicial_dimension(q,me)
  nq=q.shape[0]
  if (dim==2):
    if (scalars is None) or (plane):
      Z=np.zeros((nq,1))
    else:
      Z=scalars.reshape((nq,1))
    q=np.hstack((q,Z))
  ug = tvtk.UnstructuredGrid(points=q)
  ug.set_cells(get_cell_type(d), me)
  if scalars is not None:
    ug.point_data.scalars = scalars
    ug.point_data.scalars.name=scalars_name
  if vectors is not None:
    if vectors.shape[0]==3:
      vectors=vectors.T
    ug.point_data.vectors = vectors
    ug.point_data.vectors.name=vectors_name
  return ug

def get_cell_type(d):
  if d==1:
    return tvtk.Line().cell_type
  if d==2:
    return tvtk.Triangle().cell_type
  if d==3:
    return tvtk.Tetra().cell_type
  assert False, "Unknow cell_type for %d-simplicial element"%d

def move_mesh(q,U):
  if U is None:
    return q
  assert U.shape==q.shape
  return q+U 

#def getLocalValue(sTh,u):    
  #if len(u)==sTh.nqGlobal:
    #U=u[sTh.toGlobal]
  #elif len(u)==sTh.nqParent:
    #U=u[sTh.toParent]
  #else:
    #assert( len(u) == sTh.nq )
    #U=u
  #return U.ravel()