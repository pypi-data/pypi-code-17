# Run with: from fc_vfemp1.samples import BVPStationaryConvectionDiffusion2D01
import numpy as np
from fc_vfemp1.examples.set_examples import setBVPStationaryConvectionDiffusion2D01
bvp,info=setBVPStationaryConvectionDiffusion2D01(120,verbose=2)
u=bvp.solve()


from fc_tools.graphics import isMayavi,isMatplotlib
Th=bvp.Th
if isMayavi():
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)
  mlab.figure(1)
  simlab.plotmesh(Th,legend=True)
  mlab.view(0,0)
  mlab.figure(2)
  simlab.plotmesh(Th,d=1,line_width=2,legend=True)
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  mlab.view(0,0)
  mlab.figure(3)
  simlab.plot(Th,u)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  mlab.figure(4)
  simlab.plotiso(Th,u,contours=15)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  
if isMatplotlib():
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=4)
  plt.figure(1)
  siplt.plotmesh(Th,legend=True)
  siplt.plotmesh(Th,d=1,linewidths=2,color='Black')
  set_axes_equal()
  plt.figure(2)
  siplt.plotmesh(Th,d=1,linewidths=2,legend=True)
  siplt.plotmesh(Th,color='LightGray',alpha=0.05)
  set_axes_equal()
  plt.figure(3)
  siplt.plot(Th,u)
  plt.colorbar(label='u')
  plt.axis('off');set_axes_equal()
  plt.figure(4)
  siplt.plotiso(Th,u,contours=15)
  plt.colorbar(label='u')
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  plt.axis('off');set_axes_equal()
  