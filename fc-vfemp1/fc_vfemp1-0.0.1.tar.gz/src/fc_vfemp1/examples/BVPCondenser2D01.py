import numpy as np

from fc_vfemp1.operators import Loperator
from fc_vfemp1.examples.set_examples import setBVPCondenser2D01
from fc_vfemp1 import FEM
from fc_tools.others import isModuleFound

bvp,info=setBVPCondenser2D01(20,verbose=2)
u=bvp.solve()

Th=bvp.Th
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
  simlab.plot(Th,u,plane=False)
  simlab.plotiso(Th,u,contours=25,color='white',line_width=2,plane=False)
  #mlab.view(0,0)
  cb=mlab.colorbar(title='u',orientation='vertical')
  #cb.lut_mode='viridis'

  mlab.figure(4)
  simlab.plotiso(Th,u,contours=25)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  simlab.plotmesh(Th,d=1,color='black',line_width=1.5)

if isModuleFound('fc_simesh_matplotlib'):  
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  plt.figure(1)
  siplt.plotmesh(Th,legend=True)
  set_axes_equal()
  
  plt.figure(2)
  siplt.plotmesh(Th,d=1,legend=True,linewidth=2)
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  set_axes_equal()

  plt.figure(3)
  hp=siplt.plot(Th,u,plane=False)
  plt.colorbar(hp,label='u')
  # siplt.plotiso(Th,u,contours=25,color='white',linewidth=2,plane=False)
  plt.axis('off')#;set_axes_equal()

  plt.figure(4)
  pi=siplt.plotiso(Th,u,contours=25)
  plt.colorbar(pi,label='u')
  siplt.plotmesh(Th,color='LightGray',alpha=0.05)
  siplt.plotmesh(Th,d=1,color='black',linewidth=1.5)
  plt.axis('off');set_axes_equal()

  DisplayFigures()
