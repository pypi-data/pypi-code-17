import numpy as np
from fc_vfemp1.operators import Loperator,Hoperator
from fc_vfemp1.BVP import BVP,PDE
from fc_simesh.siMesh import HyperCube
from fc_tools.others import isModuleFound

from numpy import cos,sin
E=21e5;nu=0.45;L=20;N=10
mu= E/(2*(1+nu))
lam = E*nu/((1+nu)*(1-2*nu))
gam=lam+2*mu
uex=[lambda x,y: cos(2*x+y), lambda x,y: sin(x-3*y)]
f=[lambda x,y: 4*lam*cos(2*x + y) + 9*mu*cos(2*x + y) + 3*lam*sin(-x + 3*y) + 3*mu*sin(-x + 3*y) ,
    lambda x,y: 2*lam*cos(2*x + y) + 2*mu*cos(2*x + y) - 9*lam*sin(-x + 3*y) - 19*mu*sin(-x + 3*y)]
g2=[lambda x,y: -3*lam*cos(-x + 3*y) - 2*lam*sin(2*x + y) - 4*mu*sin(2*x + y), 
    lambda x,y: mu*(cos(-x + 3*y) - sin(2*x + y))]
print('------------------------------------------------------') 
print('      2D elasticity BVP on [0,%g]x[-1,1]'%L)
print('         on transform hypercube mesh\n')
print('             -div(sigma(u)) = f ')
print(' and boundary conditions :')
print('   * Dirichlet on [1]')
print('       u_1 = u_2 = 0 on [1],')
print('   * Neumann on [2,3,4]')
print('       sigma(u).n = 0 on [2,3,4]')
print(' with f=(0,-1)^t, lambda=%g, mu=%g\n'%(lam,mu));
print('------------------------------------------------------')
print('1. Setting the mesh using HyperCube function')
mapping=lambda q: np.array([L*q[0],-1+2*q[1]])
Th=HyperCube(2,[2*N,20*N],mapping=mapping)
print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
print('2.a Setting 2D Elasticity B.V.P. problem')

Hop=Hoperator(dim=2,d=2,m=2)
Hop.H[0][0]=Loperator(d=2,A=[[gam,None],[None,mu]]) 
Hop.H[0][1]=Loperator(d=2,A=[[None,lam],[mu,None]]) 
Hop.H[1][0]=Loperator(d=2,A=[[None,mu],[lam,None]]) 
Hop.H[1][1]=Loperator(d=2,A=[[mu,None],[None,gam]])
pde=PDE(Op=Hop,f=[0,-1])
bvp=BVP(Th,pde=pde)
bvp.setDirichlet(1,[0,0])

print('2.b Solving 2D elasticity BVP')
U=bvp.solve(split=True)

Th=bvp.Th

normU=np.sqrt(U[0]**2+U[1]**2)

if isModuleFound('fc_simesh_mayavi'):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  scale=50;
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)

  mlab.figure(1)
  simlab.plotmesh(Th,color='LightGray',opacity=0.01)
  simlab.plotmesh(Th,d=1,legend=True,line_width=2)
  mlab.view(0,0)

  mlab.figure(2)
  simlab.plotmesh(Th,color='blue',opacity=0.01)
  simlab.plotmesh(Th,color='red',move=[scale*U[0],scale*U[1]])
  mlab.view(0,0)
  
  mlab.figure(3)
  simlab.plot(Th,normU)
  simlab.plotiso(Th,normU,contours=10,color='White',line_width=1)
  simlab.plotmesh(Th,d=1,color='black')
  mlab.view(0,0)
  mlab.colorbar(title='|U|')

if isModuleFound('fc_simesh_matplotlib'):  
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=3)
  plt.figure(1)
  siplt.plotmesh(Th,color='LightGray',alpha=0.05)
  siplt.plotmesh(Th,d=1,legend=True,linewidth=2)
  set_axes_equal()
  
  plt.figure(2)
  siplt.plotmesh(Th,color='blue',alpha=0.05)
  siplt.plotmesh(Th,color='red',move=[scale*U[0],scale*U[1]],alpha=0.1)
  set_axes_equal()
  
  plt.figure(3)
  siplt.plot(Th,normU)
  plt.colorbar(label='|u|')
  siplt.plotiso(Th,normU,contours=15,color='white',linewidth=2)
  siplt.plotmesh(Th,d=1,color='black')
  plt.axis('off');set_axes_equal()
  