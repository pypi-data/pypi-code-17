import numpy as np

import scipy.sparse.linalg as spla

import fc_oogmsh
from fc_vfemp1.operators import Loperator,Hoperator
from fc_vfemp1.BVP import BVP,PDE
from fc_vfemp1.FEM import Apply
from fc_simesh.siMesh import siMesh
from fc_vfemp1.examples.set_examples import func2str
from fc_tools.others import isModuleFound

# set solver
#solver=lambda A,b: spla.bicg(A,b,tol=1e-9)
solver=lambda A,b: spla.spsolve(A,b)
from scipy.sparse.csgraph import reverse_cuthill_mckee
perm=lambda A: reverse_cuthill_mckee(A)

def set_datas(N):
  dim=3
  gD=lambda x,y,z: 10*(np.abs(z-1)>0.5)
  a=lambda x,y,z: 1+(z-1)**2
  b=0.01
  geofile='cylinderkey.geo'
  print('------------------------------------------------------') 
  print('      3D stationary heat and flow velocity BVPs')
  print('         on GMSH mesh from %s.geo'%geofile)
  print(' 1) 3D velocity potential BVP, (unknow phi)')
  print('               - Delta phi = 0')
  print('    and boundary conditions :')
  print('      * Dirichlet on [1020,1021,2020,2021]')
  print('          phi = -1 on [1020,2020], ')
  print('          phi = +1 on [1021,2021], ')
  print('      * Neumann on [1,10,11,31,1000,2000]')
  print('          du/dn = 0 on [1,10,11,31,1000,2000]')
  print('    (Velocity V = grad phi ) ')
  print(' 2) 3D stationary heat with potential flow BVP, (unknow u)')
  print('               - div(a grad u) + <V,grad u> + b u = 0')
  print(' and boundary conditions :')
  print('   * Dirichlet on [30,1020,2020]')
  print('       u = gD on [30], ')
  print('       u = 30  on [1020,2020]')
  print('   * Neumann on [others]')
  print('       du/dn = 0 on [others]')
  print(' with ')
  print('   a  = %s '%func2str(a))
  print('   b  = %g '%b)
  print('   gD = %s '%func2str(gD))
  print('------------------------------------------------------')
  print('*** Building the mesh using GMSH')
  meshfile=fc_oogmsh.gmsh.buildmesh3d(geofile,N,force=True)
  Th=siMesh(meshfile)
  print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  return dim,a,b,gD,geofile,Th


def method1(N=20,**kwargs):
  ismayavi_plot=kwargs.pop('mayavi',isModuleFound('fc_simesh_mayavi'))
  ismatplotlib_plot=kwargs.pop('matplotlib',isModuleFound('fc_simesh_matplotlib') and not ismayavi_plot)
  solver=kwargs.pop('solver',lambda A,b: spla.spsolve(A,b))
  perm=kwargs.pop('perm',lambda A: reverse_cuthill_mckee(A))
  dim,a,b,gD,geofile,Th=set_datas(N)
  print('*** Setting 3D velocity potential BVP')
  Lop=Loperator(dim=dim,A=[[1,None,None],[None,1,None],[None,None,1]])
  bvpFlow=BVP(Th,pde=PDE(Op=Lop))
  bvpFlow.setDirichlet(1021,1.)
  bvpFlow.setDirichlet(2021,1.)
  bvpFlow.setDirichlet(1020,-1.)
  bvpFlow.setDirichlet(2020,-1.)
  print('*** Solving 3D potential velocity/flow BVP')
  phi=bvpFlow.solve(perm=perm)#solver=solver) 

  print('*** Computing 3D velocity flow V')
  print('***  1) Computing V[0]')
  V=[None,None,None]
  Lop=Loperator(dim=dim,c=[1,0,0])
  V[0]=Apply(Lop,Th,phi,solver=solver,perm=perm)
  print('***  2) Computing V[1]')
  Lop=Loperator(dim=dim,c=[0,1,0])
  V[1]=Apply(Lop,Th,phi,solver=solver,perm=perm)
  print('***  3) Computing V[2]')
  Lop=Loperator(dim=dim,c=[0,0,1])
  V[2]=Apply(Lop,Th,phi,solver=solver,perm=perm)
  V=np.array(V)
  print('*** Set 3D stationnary heat BVP with potential flow')
  Lop=Loperator(dim=dim,A=[[a,None,None],[None,a,None],[None,None,a]],c=V,a0=b)
  bvpHeat=BVP(Th,pde=PDE(Op=Lop))
  bvpHeat.setDirichlet(1020,30.)
  bvpHeat.setDirichlet(2020,30.)
  bvpHeat.setDirichlet(10, gD)
  print('*** Solve 3D stationnary heat BVP with potential flow')
  u=bvpHeat.solve(perm=perm)
  
  if isModuleFound('fc_simesh_mayavi') and ismayavi_plot:
    print('*** Graphic representations using Mayavi')
    mayavi_plot(Th,phi,V,u)
  if isModuleFound('fc_simesh_matplotlib') and ismatplotlib_plot:  
    print('*** Graphic representations using Matplotlib')
    matplotlib_plot(Th,phi,V,u)
  return Th,phi,V,u

def method2(N=20,**kwargs):
  solver=kwargs.pop('solver',lambda A,b: spla.spsolve(A,b))
  perm=kwargs.pop('perm',lambda A: reverse_cuthill_mckee(A))
  ismayavi_plot=kwargs.pop('mayavi',isModuleFound('fc_simesh_mayavi'))
  ismatplotlib_plot=kwargs.pop('matplotlib',isModuleFound('fc_simesh_matplotlib') and not ismayavi_plot)
  dim,a,b,gD,geofile,Th=set_datas(N)
  print('*** Setting 3D potential velocity/flow BVP')
  Hop=Hoperator(dim=d,m=4)
  Hop.H[0][1]=Loperator(dim=dim,b=[-1,0,0])
  Hop.H[0][2]=Loperator(dim=dim,b=[0,-1,0])
  Hop.H[0][3]=Loperator(dim=dim,b=[0,0,-1])
  Hop.H[1][0]=Loperator(dim=dim,c=[-1,0,0])
  Hop.H[1][1]=Loperator(dim=dim,a0=1)
  Hop.H[2][0]=Loperator(dim=dim,c=[0,-1,0])
  Hop.H[2][2]=Loperator(dim=dim,a0=1)
  Hop.H[3][0]=Loperator(dim=dim,c=[0,0,-1])
  Hop.H[3][3]=Loperator(dim=dim,a0=1)
  bvp=BVP(Th,pde=PDE(Op=Hop))
  bvp.setDirichlet(1021,1.,comps=[0])
  bvp.setDirichlet(2021,1.,comps=[0])
  bvp.setDirichlet(1020,-1.,comps=[0])
  bvp.setDirichlet(2020,-1.,comps=[0])
  print('*** Solving 3D potential velocity/flow BVP')
  U=bvp.solve(split=True,perm=perm,solver=solver) 
  V=np.array([U[1],U[2],U[3]])
  phi=U[0] 
  print('*** Set 3D stationnary heat BVP with potential flow')
  Lop=Loperator(dim=dim,A=[[a,None,None],[None,a,None],[None,None,a]],c=V,a0=b)
  bvpHeat=BVP(Th,pde=PDE(Op=Lop))
  bvpHeat.setDirichlet(1020,30.)
  bvpHeat.setDirichlet(2020,30.)
  bvpHeat.setDirichlet(10, gD)
  print('*** Solve 3D stationnary heat BVP with potential flow')
  u=bvpHeat.solve(perm=perm)
  
  if isModuleFound('fc_simesh_mayavi') and ismayavi_plot:
    print('*** Graphic representations using Mayavi')
    mayavi_plot(Th,phi,V,u)
  if isModuleFound('fc_simesh_matplotlib') and ismatplotlib_plot:  
    print('*** Graphic representations using Matplotlib')
    matplotlib_plot(Th,phi,V,u)
  return Th,phi,V,u

def mayavi_plot(Th,phi,V,u):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_tools.mayavi import title
  VelocityMagnitude=np.sqrt(V[0]**2+V[1]**2+V[2]**2)
  mV=max(VelocityMagnitude)
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)
  mlab.figure(1)
  simlab.plotmesh(Th,d=2,legend=True)
  mlab.figure(2)
  simlab.plotmesh(Th,d=2,legend=True)
  mlab.view(17.6,160,5.6)
  
  mayavi_plotscalar(Th,u,V,'jet','u')
  mayavi_plotscalar(Th,phi,V,'viridis','phi')
  
  mlab.figure()
  simlab.quiver(Th,V,scale_factor=2*Th.get_h()/mV,mask_points=max(1,Th.nq//10000),colormap='hsv')
  simlab.plotmesh(Th,d=2,labels=[10,11,31],color='LightGray',representation='surface')
  simlab.plotmesh(Th,d=1,color='Black')
  mlab.view(5.2, 75,distance=7)
  mlab.vectorbar(title='|V|',orientation='vertical')
  
  mlab.figure()
  simlab.quiver(Th,V,scalars=u,scale_factor=2*Th.get_h()/mV,mask_points=max(1,Th.nq//10000),colormap='jet')
  simlab.plotmesh(Th,d=2,labels=[10,11,31],color='LightGray',representation='surface')
  simlab.plotmesh(Th,d=1,color='Black')
  mlab.view(5.2, 75,distance=7)
  mlab.colorbar(title='u',orientation='vertical')
  
def mayavi_plotscalar(Th,scalar,V,colormap,stitle):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_tools.mayavi import title
  mlab.figure()
  simlab.plot(Th,scalar,d=2,colormap=colormap)
  mlab.colorbar(title=stitle,orientation='vertical')
  simlab.plotmesh(Th,d=1,color='black',line_width=3)
  simlab.plotiso(Th,scalar,d=2,contours=20,color='white',line_width=2)
  
  mlab.figure()
  simlab.plot(Th,scalar,colormap=colormap,opacity=0.03)
  simlab.slice(Th,scalar,origin=[0,0,1],normal=[0,1,1],colormap=colormap)
  simlab.sliceiso(Th,scalar,origin=[0,0,1],normal=[0,1,1],contours=10,color='white')
  simlab.plot(Th,scalar,d=2,labels=[1000,2000],colormap=colormap)
  simlab.plotiso(Th,scalar,d=2,labels=[1000,2000],contours=20,color='white')
  simlab.plot(Th,scalar,d=2,labels=[10,11,31],representation='wireframe',colormap=colormap)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
  cb=mlab.colorbar(title=stitle,orientation='vertical')

  mlab.figure()
  simlab.plot(Th,scalar,colormap=colormap,opacity=0.03)
  simlab.plot(Th,scalar,d=2,labels=[10,11,31,1000,1020,1021,2000,2020,2021],colormap=colormap)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
  simlab.plotiso(Th,scalar,d=2,labels=[10,11,31,1000,1020,1021,2000,2020,2021],contours=20,color='white')
  simlab.slice(Th,scalar,origin=[0,0,1],normal=[0,0,1],colormap=colormap)
  simlab.sliceiso(Th,scalar,origin=[0,0,1],normal=[0,0,1],contours=20,color='white')
  mlab.colorbar(title=stitle,orientation='vertical')
  mlab.view(-14.95, 68.35,distance=6.70)#,focalpoint=(-0.65,0.,0.))
  
  mlab.figure()
  sw_options={'center':np.array([0.9,0,1]), 'radius':0.1,'phi_resolution':8,'theta_resolution':12,'enabled':True}#'handle_visibility':False}
  st_options={'integration_direction':'both'}
  sl1=simlab.streamline(Th,scalar,V,scalars_name='heat',colormap=colormap,seed_widget_options=sw_options,streamtracer_options=st_options)
  simlab.plotmesh(Th,d=2,color='LightGray',opacity=0.05)
  simlab.plotmesh(Th,d=1,color='black',line_width=2)
  sw_options['center']=np.array([-0.9,0,1])
  sl2=simlab.streamline(Th,scalar,V,scalars_name='heat',colormap=colormap,seed_widget_options=sw_options,streamtracer_options=st_options)
  mlab.scalarbar(title=stitle,orientation='vertical')
  mlab.view(32,70.6,6.7)  

def matplotlib_plot(Th,phi,V,u):
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  VelocityMagnitude=np.sqrt(V[0]**2+V[1]**2+V[2]**2)
  mV=max(VelocityMagnitude)
  plt.close('all')
  plt.ion()
  labels=np.setdiff1d(Th.sThlab[Th.find(2)],1) # except label 1
  
  plt.figure()
  siplt.plotmesh(Th,d=2,legend=True)
  set_axes_equal()
  
  plt.figure()
  siplt.plotmesh(Th,d=2,legend=True,labels=labels)
  set_axes_equal()
  
  plt.figure()
  sp=siplt.plot(Th,u,colormap='jet')
  plt.colorbar(sp,label='$u$ ')
  plt.axis('off');set_axes_equal()
  
  plt.figure()
  sp=siplt.plot(Th,u,d=2,labels=labels,colormap='jet')
  plt.colorbar(sp,label='$u$ ')
  siplt.plotmesh(Th,d=1,color='Black')
  plt.axis('off');set_axes_equal()
  
  plt.figure()
  sp=siplt.plot(Th,phi)
  plt.colorbar(sp,label='$\phi$ ')
  plt.axis('off');set_axes_equal()
  
  plt.figure()
  sp=siplt.plot(Th,phi,d=2,labels=labels)
  plt.colorbar(sp,label='$\phi$ ')
  siplt.plotmesh(Th,d=1,color='Black')
  plt.axis('off');set_axes_equal()
    
  fig=plt.figure()
  sp=siplt.quiver(Th,V,scale_factor=2*Th.get_h()/mV,nvec=5000,colormap='hsv')
  plt.colorbar(sp,label='$||V||$ ')
  siplt.plotmesh(Th,d=2,labels=[10,11,31],color='LightGray')
  siplt.plotmesh(Th,d=1,color='Black')
  fig.axes[0].elev=-150 # or fig.axes[0].view_init(elev,azim)
  fig.axes[0].azim=0.3
  fig.axes[0].dist=7.5
  plt.axis('off');set_axes_equal()
  
  fig=plt.figure()
  sp=siplt.quiver(Th,V,scalars=u,scale_factor=2*Th.get_h()/mV,nvec=5000,colormap='jet')
  plt.colorbar(sp,label='$u$ ')
  siplt.plotmesh(Th,d=2,labels=[10,11,31],color='LightGray')
  siplt.plotmesh(Th,d=1,color='Black')
  fig.axes[0].elev=-150 # or fig.axes[0].view_init(elev,azim)
  fig.axes[0].azim=0.3
  fig.axes[0].dist=7.5
  plt.axis('off');set_axes_equal()
  
  DisplayFigures()