import numpy as np
from fc_vfemp1.operators import StiffElasHoperator
from fc_vfemp1.BVP import BVP,PDE
from fc_simesh.siMesh import HyperCube
from fc_tools.others import isModuleFound

E=21e5;nu=0.45;L=20;N=10
mu= E/(2*(1+nu))
lam = E*nu/((1+nu)*(1-2*nu))
gam=lam+2*mu
L=5;N=7
print('------------------------------------------------------')
print('      3D elasticity BVP on [0,%g]x[0,1]x[0,1]'%L);
print('         on transform hypercube mesh')
print('             -div(sigma(u)) = f ')
print(' and boundary conditions :')
print('   * Dirichlet on [1]')
print('       u_1 = u_2 = 0 on [1],')
print('   * Neumann on [2,3,4,5,6]')
print('       sigma(u).n = 0 on [2,3,4,5,6]')
print(' with f=(0,0,-1)^t, lambda=%g, mu=%g'%(lam,mu))
print('------------------------------------------------------')
mapping=lambda q: np.array([L*q[0],q[1],q[2]])
Th=HyperCube(3,[L*N,N,N],mapping=mapping)
print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
print('2.a Setting 3D Elasticity B.V.P. problem')

Hop=StiffElasHoperator(3,lam,mu)
pde=PDE(Op=Hop,f=[0,0,-1])
bvp=BVP(Th,pde=pde)
bvp.setDirichlet(1,[0,0,0])

print('2.b Solving 3D elasticity BVP')
U=bvp.solve(split=True)

Th=bvp.Th

normU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)

if isModuleFound('fc_simesh_mayavi'):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  scale=2000
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)

  mlab.figure(1)
  simlab.plotmesh(Th,d=2,legend=True)
  
  mlab.figure(2)
  simlab.plotmesh(Th,color='blue',opacity=0.01)
  simlab.plotmesh(Th,color='red',move=[scale*U[0],scale*U[1],scale*U[2]])
  
  mlab.figure(3)
  simlab.plot(Th,normU,d=2)
  simlab.plotiso(Th,normU,d=2,contours=10,color='White',line_width=1)
  simlab.plotmesh(Th,d=1,color='black')
  mlab.colorbar(title='|U|')

if isModuleFound('fc_simesh_matplotlib'):  
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=3)
  plt.figure(1)
  siplt.plotmesh(Th,d=2,legend=True)
  set_axes_equal()
  
  plt.figure(2)
  siplt.plotmesh(Th,color='blue',alpha=0.05)
  siplt.plotmesh(Th,color='red',move=[scale*U[0],scale*U[1],scale*U[2]],alpha=0.1)
  plt.axis('off');set_axes_equal()
  
  plt.figure(3)
  hp=siplt.plot(Th,normU,d=2)
  plt.colorbar(hp,label='|u|')
  siplt.plotmesh(Th,d=1,color='black')
  plt.axis('off');set_axes_equal()
  