import numpy as np

from fc_vfemp1.operators import Loperator
from fc_vfemp1.examples import set_examples
from fc_vfemp1.examples.set_examples import *
from fc_vfemp1 import FEM
from fc_tools.others import isModuleFound

def BVPElectrostatic2D01(**kwargs):
  N=kwargs.pop('N',80)
  kwargs['sigma1']=kwargs.get('sigma1',1)
  kwargs['sigma2']=kwargs.get('sigma2',10)
  isMayavi=kwargs.pop('mayavi',isModuleFound('fc_simesh_mayavi'))
  isMatplotlib=kwargs.pop('matplotlib',isModuleFound('fc_simesh_matplotlib'))
  bvp,info=set_examples.setBVPElectrostatic2D01(N,**kwargs)
  u=bvp.solve()
  Th=bvp.Th
  E=np.zeros((2,Th.nq))
  Lop=Loperator(dim=2,d=2,c=[1,0])
  E[0]=FEM.Apply(Lop,Th,u)#,solver=solver,perm=perm)
  Lop=Loperator(dim=2,d=2,c=[0,1])
  E[1]=FEM.Apply(Lop,Th,u)#,solver=solver,perm=perm)
  ENorm=np.sqrt(E[0]**2+E[1]**2)
   
  def BVPElectrostatic2D01_mayavi(Th,u,E,ENorm):
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
    simlab.plot(Th,u,colormap='viridis')
    simlab.plotiso(Th,u,contours=25,color='white',line_width=1)
    simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
    mlab.view(0,0)
    mlab.colorbar(title='u',orientation='vertical')

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
    mlab.colorbar(title='||E||',orientation='vertical')
    
    mlab.figure(6)
    simlab.plotiso(Th,ENorm,contours=25,colormap='jet')
    mlab.view(0,0)
    mlab.colorbar(title='||E||',orientation='vertical')
    simlab.plotmesh(Th,color='LightGray',opacity=0.05)
    simlab.plotmesh(Th,d=1,color='black',line_width=1.5)

    mlab.figure(7)
    simlab.quiver(Th,E,scale_factor=0.3e-3)
    mlab.colorbar(title='E',orientation='vertical')
    simlab.plotmesh(Th,d=1,color='black',line_width=1.5)
    mlab.view(0,0)

  def BVPElectrostatic2D01_matplotlib(Th,u,E,ENorm):
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
    siplt.plot(Th,u,colormap='viridis')
    plt.colorbar(label='u')
    siplt.plotiso(Th,u,contours=25,color='white',linewidth=2)
    plt.axis('off');set_axes_equal()

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
    
  if isMayavi:
    BVPElectrostatic2D01_mayavi(Th,u,E,ENorm)
  if isMatplotlib:
    BVPElectrostatic2D01_matplotlib(Th,u,E,ENorm)
  return {'bvp':bvp,'u':u,'E':E}

def BVPPoisson2D(**kwargs):
  kwargs['verbose']=kwargs.get('verbose',2)
  version=kwargs.pop('version','ex01')
  N=kwargs.pop('N',50)
  isMayavi=kwargs.pop('mayavi',isModuleFound('fc_simesh_mayavi'))
  isMatplotlib=kwargs.pop('matplotlib',isModuleFound('fc_simesh_matplotlib'))
  bvp,info=globals()['setBVPPoisson2D_'+version](N,**kwargs)
  verbose=kwargs.get('verbose',1)
  if verbose>0:
    print("*** Solving BVP")
  u,err,errL2,errH1=SolvePoisson2Dex(bvp,info)
  if verbose>0:
    print("  Error L2: %e, Error H1: %e\n"%(errL2,errH1))
  Th=bvp.Th  
  if isMayavi:
    BVPPoisson2D_mayavi(Th,u,err)
  if isMatplotlib:
    BVPPoisson2D_matplotlib(Th,u,err)
  return {'bvp':bvp,'info':info,'u':u,'errH1':errH1,'errL2':errL2}
    
def SolvePoisson2Dex(bvp,info):
  u=bvp.solve()
  Th=bvp.Th
  uex=info['solex']
  Uex=Th.feval(uex)
  err=np.abs(u-Uex)
  errH1,M,K=FEM.NormH1(Th,err)
  errH1=errH1/FEM.NormH1(Th,u,Mass=M,Stiff=K)[0]
  errL2=FEM.NormL2(Th,err,Mass=M)[0]/FEM.NormL2(Th,u,Mass=M)[0]
  return u,err,errL2,errH1
    
def BVPPoisson2D_mayavi(Th,u,err):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  if len(mlab.get_engine().scenes)>0:
    mlab.close(all=True)
  mlab.figure(1)
  simlab.plot(Th,u)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')

  mlab.figure(2)
  simlab.plotiso(Th,u,contours=15)
  mlab.view(0,0)
  mlab.colorbar(title='u',orientation='vertical')
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)

  mlab.figure(3)
  simlab.plot(Th,err,colormap='jet')
  mlab.view(0,0)
  mlab.colorbar(title='error',orientation='vertical')

  mlab.figure(4)
  simlab.plotiso(Th,err,contours=15,colormap='jet')
  mlab.view(0,0)
  t=mlab.colorbar(title='error',orientation='vertical')
  t.label_text_property.font_size=16 # ??? don't work
  simlab.plotmesh(Th,color='LightGray',opacity=0.05)
  
def BVPPoisson2D_matplotlib(Th,u,err):
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=4)
  plt.figure(1)
  siplt.plot(Th,u)
  plt.colorbar(label='u')
  set_axes_equal()

  plt.figure(2)
  siplt.plotiso(Th,u,contours=15)
  plt.colorbar(label='u')
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  plt.axis('off');set_axes_equal()

  plt.figure(3)
  siplt.plot(Th,err,colormap='jet')
  plt.colorbar(label='error')
  plt.axis('off');set_axes_equal()

  plt.figure(4)
  siplt.plotiso(Th,err,contours=15,colormap='jet')
  plt.colorbar(label='error')
  siplt.plotmesh(Th,color='LightGray',alpha=0.3)
  plt.axis('off');set_axes_equal()
  plt.show()