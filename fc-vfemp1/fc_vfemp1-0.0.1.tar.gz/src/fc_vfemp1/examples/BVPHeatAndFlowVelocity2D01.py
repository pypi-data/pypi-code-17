import numpy as np

import fc_oogmsh
from fc_vfemp1.operators import Loperator,Hoperator
from fc_vfemp1.BVP import BVP,PDE
from fc_simesh.siMesh import siMesh
from fc_vfemp1.examples.set_examples import func2str
from fc_tools.others import isModuleFound
from fc_tools.mayavi import mlab_latex3D

__all__ = ['method1','method2']

def set_datas(N):
  dim=2
  af=lambda x,y: 0.1+y**2
  gD=lambda x,y: 20*y
  b=0.01
  geofile='disk5holes.geo'

  print('------------------------------------------------------') 
  print('      2D stationary heat and flow velocity BVPs')
  print('         on GMSH mesh from %s.geo'%geofile)
  print(' 1) 2D velocity potential BVP, (unknow phi)')
  print('               - Delta phi = 0')
  print('    and boundary conditions :')
  print('      * Dirichlet on [20,21]')
  print('          phi = -20 on [21], 20 on [20]')
  print('      * Neumann on [1,22,23]')
  print('          du/dn = 0 on [1,22,23]')
  print('    (Velocity V = grad phi ) ')
  print(' 2) 2D stationary heat with potential flow BVP, (unknow u)')
  print('               - div(a grad u) + <V,grad u> + b u = f')
  print(' and boundary conditions :')
  print('   * Dirichlet on [21,22,23]')
  print('       u = gD on [21], 0 on [22] and 0 on [23]  ')
  print('   * Neumann on [1,10,20]')
  print('       du/dn = 0 on [1,10,20]')
  print(' with ')
  print('   a = %s '%func2str(af))
  print('   b = %s '%func2str(b))
  print('   gD = %s '%func2str(gD))
  print('------------------------------------------------------')
  
  print('*** Building the mesh using GMSH')
  meshfile=fc_oogmsh.gmsh.buildmesh2d(geofile,N,force=True)
  Th=siMesh(meshfile)
  print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  return dim,af,gD,b,geofile,Th
  
def method1(N=60):
  dim,af,gD,b,geofile,Th=set_datas(N)
  print('*** Setting 2D velocity potential BVP')
  Lop=Loperator(dim=dim,A=[[1,None],[None,1]])
  bvpVelocityPotential=BVP(Th,pde=PDE(Op=Lop))
  bvpVelocityPotential.setDirichlet(20,+20.)
  bvpVelocityPotential.setDirichlet(21,-20.)
  print('*** Solving 2D velocity potential BVP')
  phi=bvpVelocityPotential.solve()
  print('*** Setting 2D potential flow operator')
  Hop=Hoperator(dim=dim,m=2)
  Hop.H[0][0]=Loperator(dim=dim,c=[1,0])
  Hop.H[1][1]=Loperator(dim=dim,c=[0,1])
  print('*** Applying 2D potential flow operator')
  V=Hop.apply(Th,[phi,phi])
  print('*** Setting 2D stationary heat BVP with potential flow')
  Lop=Loperator(dim=dim,A=[[af,None],[None,af]],c=V,a0=b)
  bvpHeat=BVP(Th,pde=PDE(Op=Lop))
  bvpHeat.setDirichlet(21,gD)
  bvpHeat.setDirichlet(22, 0)
  bvpHeat.setDirichlet(23, 0)
  print('*** Solving 2D stationary heat BVP with potential flow')
  u=bvpHeat.solve()

  if isModuleFound('fc_simesh_mayavi'):
    print('*** Graphic representations using Mayavi')
    mayavi_plot(Th,phi,V,u)
  if isModuleFound('fc_simesh_matplotlib'):  
    print('*** Graphic representations using Matplotlib')
    matplotlib_plot(Th,phi,V,u)
  return Th,phi,V,u

def method2(N=60):
  dim,af,gD,b,geofile,Th=set_datas(N)
  print('*** Setting 2D potential velocity/flow BVP')
  Hop=Hoperator(dim=dim,m=3)
  Hop.H[0][1]=Loperator(dim=dim,b=[-1,0])
  Hop.H[0][2]=Loperator(dim=dim,b=[0,-1])
  Hop.H[1][0]=Loperator(dim=dim,c=[-1,0])
  Hop.H[1][1]=Loperator(dim=dim,a0=1)
  Hop.H[2][0]=Loperator(dim=dim,c=[0,-1])
  Hop.H[2][2]=Loperator(dim=dim,a0=1)
  bvpFlow=BVP(Th,pde=PDE(Op=Hop))
  bvpFlow.setDirichlet(20,20,comps=[0])
  bvpFlow.setDirichlet(21,-20,comps=[0])
  print('*** Solving 2D potential velocity/flow BVP')
  U=bvpFlow.solve(split=True) 
  print('*** Setting 2D stationary heat BVP with potential flow')
  V=np.array([U[1],U[2]])
  phi=U[0] 
  Lop=Loperator(dim=d,d=d,A=[[af,None],[None,af]],c=V,a0=b)
  bvpHeat=BVP(Th,PDEelt(Lop))
  bvpHeat.setDirichlet(21,gD)
  bvpHeat.setDirichlet(22, 0)
  bvpHeat.setDirichlet(23, 0)
  print('*** Solving 2D stationary heat BVP with potential flow')
  u=bvpHeat.solve()
  
  if isModuleFound('fc_simesh_mayavi'):
    print('*** Graphic representations using Mayavi')
    mayavi_plot(Th,phi,V,u)
  if isModuleFound('fc_simesh_matplotlib'):  
    print('*** Graphic representations using Matplotlib')
    matplotlib_plot(Th,phi,V,u)
  return Th,phi,V,u

def mayavi_plot(Th,phi,V,u):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_tools.mayavi import title
  v2=np.sqrt(V[0]**2+V[1]**2)
  mv2=np.max(v2)

  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)
  mlab.figure(1)
  simlab.plotmesh(Th,color='LightGray',opacity=0.3)
  simlab.plotmesh(Th,d=1,legend=True)
  mlab.view(0,0)
  
  textproperty={'bold':True,'font_size':16,'shadow':True}
  latex_property={'color':'Black','center':(0,1.2,0)}

  mlab.figure(2)
  simlab.plot(Th,u,colormap='jet')
  simlab.plotiso(Th,u,contours=np.arange(1,17),color='white',line_width=1,opacity=0.5)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  mlab_latex3D('2D stationary heat with potentiel flow',width=2,**latex_property)
  
  mlab.figure(3)
  simlab.plot(Th,phi)
  mlab.colorbar(title='phi',orientation='vertical')
  simlab.plotiso(Th,phi,contours=15,color='white',line_width=1,opacity=0.5)
  mlab.view(0,0)
  #simlab.plotmesh(Th,d=1,color='Black',line_width=2)
  mlab_latex3D('Velocity potential $\phi$',width=1.2,**latex_property)
  
  mlab.figure(4)
  simlab.plot(Th,v2)
  mlab.colorbar(title='|V|',orientation='vertical')
  simlab.plotiso(Th,v2,contours=15,color='white',line_width=1,opacity=0.5)
  mlab.view(0,0)
  #simlab.plotmesh(Th,d=1,color='Black',line_width=2)
  mlab_latex3D('Norm of the potential flow $\mathbf{V}$',width=2,**latex_property)
  
  mlab.figure(5)
  simlab.quiver(Th,V,scalars=u,colormap='jet',scale_factor=0.0015,line_width=1,mask_points=Th.nq//4000)
  #mlab.vectorbar(title='Velocity')
  mlab.scalarbar(title='u',orientation='vertical')
  mlab.view(0,0)
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  simlab.plotmesh(Th,d=1,color='Black',line_width=2)
  mlab_latex3D('Potential flow $\mathbf{V}$ colorized with heat $u$',width=2,**latex_property)
  
  mlab.figure(6)
  simlab.quiver(Th,V,scalars=u,colormap='jet',scale_factor=0.0015,line_width=1,mask_points=Th.nq//4000)
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  simlab.plotmesh(Th,d=1,color='Black',line_width=2)
  mlab.view(0.0, 0.0,distance=1.1,focalpoint=(-0.65,0.,0.))

def matplotlib_plot(Th,phi,V,u):
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  v2=np.sqrt(V[0]**2+V[1]**2)
  mv2=np.max(v2)
  
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=6)

  plt.figure(1)
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  siplt.plotmesh(Th,d=1,legend=True)
  set_axes_equal()

  plt.figure(2)
  siplt.plot(Th,u,colormap='jet')
  plt.colorbar(label='$u$')
  siplt.plotiso(Th,u,isorange=np.arange(1,17),color='white',linewidth=1,alpha=0.5)
  plt.title('2D stationary heat with potentiel flow')
  plt.axis('off');set_axes_equal()

  plt.figure(3)
  siplt.plot(Th,phi)
  plt.colorbar(label='$\phi$')
  siplt.plotiso(Th,phi,niso=10,color='white',linewidth=1,alpha=0.5)
  plt.title('Velocity potential $\phi$')
  plt.axis('off');set_axes_equal()
  
  plt.figure(4)
  siplt.plot(Th,v2)
  plt.colorbar(label='$\|V\|_2$')
  siplt.plotiso(Th,v2,niso=15,color='white',linewidth=1,alpha=0.5)
  plt.title('Norm of the potential flow $V$')
  plt.axis('off');set_axes_equal()

  plt.figure(5)
  siplt.quiver(Th,V,scalars=u,scale_factor=2*Th.get_h()/mv2,nvec=Th.nq//2,colormap='jet',linewidth=1)
  plt.colorbar(label='$u$')
  plt.title('Potential flow $\mathbf{V}$ colorized with heat $u$')
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  siplt.plotmesh(Th,d=1,color='Black',linewidth=2)
  plt.axis('off');set_axes_equal()
  
  plt.figure(6)
  siplt.quiver(Th,V,scalars=u,scale_factor=2*Th.get_h()/mv2,nvec=Th.nq//2,colormap='jet',linewidth=1)
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  siplt.plotmesh(Th,d=1,color='Black',linewidth=2)
  plt.axis('off');set_axes_equal()
  plt.axis([-1, -0.2, -0.22, 0.22])
