import numpy as np

from fc_vfemp1.operators import Loperator
from fc_vfemp1.examples.set_examples import setBVPElectrostatic2D01
from fc_vfemp1 import FEM
from fc_tools.others import isModuleFound
geodir='/home/cuvelier/Travail/Recherch/python/fc-vfemp1/geodir/2d'

print(globals())
if 'sigma1' in globals():
  print('sigma1=%g'%sigma1)
  
print(locals())
if 'sigma1' in locals():
  print('sigma1=%g'%sigma1)

bvp,info=setBVPElectrostatic2D01(80,verbose=2,geodir=geodir,sigma1=10)
u=bvp.solve()

Th=bvp.Th
E=np.zeros((2,Th.nq))
Lop=Loperator(dim=2,d=2,c=[1,0])
E[0]=FEM.Apply(Lop,Th,u)#,solver=solver,perm=perm)
Lop=Loperator(dim=2,d=2,c=[0,1])
E[1]=FEM.Apply(Lop,Th,u)#,solver=solver,perm=perm)

ENorm=np.sqrt(E[0]**2+E[1]**2)

if isModuleFound('fc_simesh_mayavi'):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)

  mlab.figure(1)
  simlab.plotmesh(Th,legend=True)
  mlab.view(0,0)

  mlab.figure(2)
  simlab.plotmesh(Th,d=1,legend=True,line_width=2)
  simlab.plotmesh(Th,color='LightGray',opacity=0.3)
  mlab.view(0,0)

  mlab.figure(3)
  simlab.plot(Th,u,colormap='viridis',plane=False)
  simlab.plotiso(Th,u,contours=25,color='white',line_width=2,plane=False)
  #mlab.view(0,0)
  cb=mlab.colorbar(title='u',orientation='vertical')
  cb.lut_mode='viridis'

  mlab.figure(4)
  simlab.plotiso(Th,u,contours=25,colormap='viridis')
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)

  mlab.figure(5)
  simlab.plot(Th,ENorm,d=2,colormap='jet')
  simlab.plotiso(Th,ENorm,d=2,contours=20,color=(1,1,1),line_width=1)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
  mlab.view(0,0)

  mlab.figure(6)
  simlab.quiver(Th,E,scale_factor=0.3e-3)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
  mlab.view(0,0)

if isModuleFound('fc_simesh_matplotlib'):  
#if isMatplotlib():
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=6)
  plt.figure(1)
  siplt.plotmesh(Th,legend=True)
  set_axes_equal()
  
  plt.figure(2)
  siplt.plotmesh(Th,d=1,legend=True,linewidth=2)
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  set_axes_equal()

  plt.figure(3)
  hp=siplt.plot(Th,u,colormap='viridis',plane=False)
  plt.colorbar(hp,label='u')
  #siplt.plotiso(Th,u,contours=25,color='white',linewidth=2,plane=False)
  plt.axis('off')#;set_axes_equal()

  plt.figure(4)
  siplt.plotiso(Th,u,contours=25,colormap='viridis')
  plt.colorbar(label='u')
  siplt.plotmesh(Th,color='LightGray',alpha=0.05)
  siplt.plotmesh(Th,d=1,color='black',linewidth=1.5)
  plt.axis('off');set_axes_equal()

  plt.figure(5)
  siplt.plot(Th,ENorm,d=2,colormap='jet')
  plt.colorbar(label='$\|E\|$ ')
  siplt.plotiso(Th,ENorm,d=2,contours=20,color=(1,1,1),linewidth=1)
  siplt.plotmesh(Th,d=1,color='black',linewidth=1.5)
  plt.axis('off');set_axes_equal()

  plt.figure(6)
  siplt.quiver(Th,E,scale_factor=0.3e-3)
  plt.colorbar(label='$E$ ')
  siplt.plotmesh(Th,d=1,color='black',linewidth=1.5)
  plt.axis('off');set_axes_equal()