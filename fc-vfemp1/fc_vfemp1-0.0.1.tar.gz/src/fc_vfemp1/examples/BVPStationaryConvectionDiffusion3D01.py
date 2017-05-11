# Run with: from fc_vfemp1.examples import BVPStationaryConvectionDiffusion3D01
import numpy as np
from fc_vfemp1.examples.set_examples import setBVPStationaryConvectionDiffusion3D01
bvp,info=setBVPStationaryConvectionDiffusion3D01(20,verbose=2)
print('3. Solving BVP problem')
u=bvp.solve()

print('4. Plotting mesh and solution')
from fc_tools.others import isModuleFound
Th=bvp.Th
if isModuleFound('fc_simesh_mayavi'):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)
  mlab.figure(1)
  simlab.plotmesh(Th,legend=True)
  mlab.figure(2)
  simlab.plotmesh(Th,d=2,legend=True)
  mlab.figure(3)
  simlab.plotmesh(Th,d=2,legend=True,labels=[10,20,21,100,101])
  mlab.figure(4)
  simlab.plot(Th,u,line_width=1)
  mlab.colorbar(title='u',orientation='vertical')
  mlab.figure(5)
  simlab.plot(Th,u,d=2,labels=[10,20,21,100,101])
  simlab.plotiso(Th,u,d=2,labels=[10,20,21,100,101],contours=10,color='White')
  mlab.colorbar(title='u',orientation='vertical')
  mlab.figure(6)
  simlab.slice(Th,u,origin=(0,0,1),normal=(0,1,1))
  simlab.sliceiso(Th,u,origin=(0,0,1),normal=(0,1,1),contours=10,color='White')
  simlab.plot(Th,u,d=2,labels=[100,101])
  simlab.plotiso(Th,u,d=2,labels=[100,101],contours=10,color='White')
  simlab.plot(Th,u,d=2,labels=[10,20,21],representation='wireframe',line_width=1)
  mlab.colorbar(title='u',orientation='vertical')
  mlab.view(-49.8,73.4,7)
  
if isModuleFound('fc_simesh_matplotlib'):
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=5)
  plt.figure(1)
  siplt.plotmesh(Th,legend=True)
  set_axes_equal()
  plt.figure(2)
  siplt.plotmesh(Th,d=2,legend=True)
  set_axes_equal()
  plt.figure(3)
  siplt.plotmesh(Th,d=2,labels=[10,20,21,100,101],legend=True)
  set_axes_equal()
  plt.figure(4)
  hp=siplt.plot(Th,u)
  plt.colorbar(hp,label='u')
  plt.axis('off');set_axes_equal()
  plt.figure(5)
  hp=siplt.plot(Th,u,d=2,labels=[10,20,21,100,101])
  plt.colorbar(hp,label='u')
  plt.axis('off');set_axes_equal()
  