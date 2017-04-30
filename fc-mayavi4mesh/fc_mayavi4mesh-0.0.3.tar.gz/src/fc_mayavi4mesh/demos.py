import numpy as np
import os
from mayavi import mlab
from fc_mayavi4mesh.sys import getDataPath
import fc_mayavi4mesh.simplicial as mlab4sim

def getMesh2D(d=2):
  assert d==2 or d==1
  data_path=getDataPath()
  npzfile = np.load(data_path+os.sep+'mesh%dsimp2D.npz'%d)
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  return q,me

def getMesh3D(d=3):
  assert d==3 or d==2 or d==1
  data_path=getDataPath()
  npzfile = np.load(data_path+os.sep+'mesh%dsimp3D.npz'%d)
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  return q,me

def getMesh3Ds(d=2):
  assert d==2 or d==1
  data_path=getDataPath()
  npzfile = np.load(data_path+os.sep+'mesh%dsimp3Ds.npz'%d)
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  return q,me

def plotmesh2D():
  q2,me2=getMesh2D(2)
  q1,me1=getMesh2D(1)
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plotmesh(q2,me2)
  mlab.view(0,0)
  mlab.figure(2)
  mlab4sim.plotmesh(q1,me1,color='Red',line_width=2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.view(0,0)
  
def plotmesh3D():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plotmesh(q3,me3)
  mlab.figure(2)
  mlab4sim.plotmesh(q2,me2,color='Red')
  mlab.figure(3)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.02)
  mlab4sim.plotmesh(q1,me1,color='Magenta',line_width=2)
  from fc_tools.graphics import Plane
  P=[Plane(origin=[0,0,1],normal=[0,0,-1]), Plane(origin=[0,0,1],normal=[0,-1,-1])]
  mlab.figure(4)
  mlab4sim.plotmesh(q3,me3,cut_planes=P,color='DarkGrey')
  mlab4sim.plotmesh(q2,me2,cut_planes=P)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.view(-146,67,6)
  
def plotmesh3Ds():
  q2,me2=getMesh3Ds(2)
  q1,me1=getMesh3Ds(1)
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plotmesh(q2,me2,color='Red')
  mlab.figure(2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.02)
  mlab4sim.plotmesh(q1,me1,color='Magenta',line_width=2)
  
def plot2D():
  q2,me2=getMesh2D(2)
  q1,me1=getMesh2D(1)
  f=lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y)
  u2=f(q2[:,0],q2[:,1])
  u1=f(q1[:,0],q1[:,1])
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.view(0,0)
  mlab.figure(2)
  mlab4sim.plot(q1,me1,u1,line_width=2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(3)
  mlab4sim.plot(q2,me2,u2,plane=False)
  mlab4sim.plotmesh(q1,me1,z=u1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(4)
  mlab4sim.plot(q1,me1,u1,line_width=2,plane=False)
  mlab4sim.plotmesh(q2,me2,z=u2,color='LightGray',opacity=0.1)
  mlab.colorbar()
  
  
def plot3D():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[:,0],q3[:,1],q3[:,2])
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plot(q3,me3,u3)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(3)
  mlab4sim.plot(q1,me1,u1,line_width=2,vmin=min(u3),vmax=max(u3))
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.02)
  mlab.colorbar()
  
def plot3Ds():
  q2,me2=getMesh3Ds(2)
  q1,me1=getMesh3Ds(1)
  f=lambda x,y,z: np.cos(3*x-1)*np.sin(2*y-2)*np.sin(3*z)
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True)
  mlab.figure(1)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plot(q1,me1,u1,line_width=2,vmin=min(u2),vmax=max(u2))
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.colorbar()
  
def plotiso2D01():
  q2,me2=getMesh2D(2)
  q1,me1=getMesh2D(1)
  f=lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y)
  u2=f(q2[:,0],q2[:,1])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plotiso(q2,me2,u2,contours=25,colormap='viridis')
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab4sim.plotmesh(q2,me2,color='LightGray',representation='surface',opacity=0.4)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plot(q2,me2,u2,colormap='viridis')
  mlab4sim.plotiso(q2,me2,u2,contours=np.arange(-1,1,0.2),colormap='viridis',color='White')
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(3)
  mlab4sim.plotiso(q2,me2,u2,contours=25,colormap='viridis',plane=False)
  #mlab4sim.plotmesh(q1,me1,color='black',plane=False)
  mlab4sim.plotmesh(q2,me2,color='LightGray',representation='surface',opacity=0.4,z=u2)
  mlab.colorbar()
  mlab.figure(4)
  mlab4sim.plot(q2,me2,u2,colormap='viridis',plane=False)
  mlab4sim.plotiso(q2,me2,u2,contours=np.arange(-1,1,0.2),colormap='viridis',color='White',plane=False)
  mlab.colorbar()
  
def plotiso3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[:,0],q3[:,1],q3[:,2])
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plotiso(q2,me2,u2,line_width=2)
  mlab4sim.plotmesh(q2,me2, color='LightGray', opacity=0.1)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotiso(q2,me2,u2,line_width=2,color='White')
  mlab4sim.plotmesh(q1,me1, color='Black')
  mlab.colorbar()
  mlab.view(65,74,7)

def plotiso3Ds01():
  q2,me2=getMesh3Ds(2)
  q1,me1=getMesh3Ds(1)
  f=lambda x,y,z: np.cos(3*x-1)*np.sin(2*y-2)*np.sin(3*z)
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plot(q2,me2,u2, opacity=0.7)
  mlab4sim.plotiso(q2,me2,u2, line_width=1.5)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotiso(q2,me2,u2, line_width=1.5,color='White')
  mlab4sim.plotmesh(q1,me1, color='Black')
  mlab.colorbar()
  
def slicemesh3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.figure(2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  for normal,color in [((1,0,0),'red'),((0,1,0),'magenta'),((0,0,1),'Maroon')]:
    mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=normal,color=color)
  mlab.view(155,66,7)
  
def slice3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[:,0],q3[:,1],q3[:,2])
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.slice(q3,me3,u3,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    mlab4sim.slice(q3,me3,u3,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  
def sliceiso3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x-y)*np.sin(2*y+x)*np.sin(3*z)
  u3=f(q3[:,0],q3[:,1],q3[:,2])
  u2=f(q2[:,0],q2[:,1],q2[:,2])
  u1=f(q1[:,0],q1[:,1],q1[:,2])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.sliceiso(q3,me3,u3,origin=(0,0,1),normal=(-1,0,1))
  mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=(-1,0,1),color='DarkGray')
  mlab.view(132,53,7)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=normal, color='LightGray')
    mlab4sim.sliceiso(q3,me3,u3,contours=15,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  
def quiver2D01():
  q2,me2=getMesh2D(2)
  q1,me1=getMesh2D(1)
  f=lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y)
  u=f(q2[:,0],q2[:,1])
  w=[lambda x,y: y*np.cos(-(x**2+y**2)/10), lambda x,y: -x*np.cos(-(x**2+y**2)/10)]
  W=np.array([w[0](q2[:,0],q2[:,1]),w[1](q2[:,0],q2[:,1])])
  mlab.close(all=True) 
  nq=q2.shape[0]
  mlab.figure(1)
  mlab4sim.quiver(q2,me2,W, scale_factor=0.05 ,line_width=1, mask_points=nq//2000,colormap='viridis')
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab.vectorbar()
  mlab.view(0,0)
  mlab.figure(2)
  mlab4sim.quiver(q2,me2,W, scalars=u, scale_factor=0.05,line_width=1, mask_points=nq//2000)
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab.scalarbar()
  mlab.view(0,0)
  
def quiver3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u=f(q3[:,0],q3[:,1],q3[:,2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([w[0](q3[:,0],q3[:,1],q3[:,2]),
              w[1](q3[:,0],q3[:,1],q3[:,2]),
              w[2](q3[:,0],q3[:,1],q3[:,2])])
  mlab.close(all=True)
  nq=q3.shape[0]
  mlab.figure(1)
  mlab4sim.quiver(q3,me3,W,line_width=1, mask_points=nq//3000)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.05)
  mlab.vectorbar()
  mlab.figure(2)
  mlab4sim.quiver(q3,me3,W,scalars=u, line_width=1, mask_points=nq//3000)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.scalarbar()
  
def quiver3Ds01():
  q2,me2=getMesh3Ds(2)
  q1,me1=getMesh3Ds(1)
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  u=f(q2[:,0],q2[:,1],q2[:,2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z]
  W=np.array([w[0](q2[:,0],q2[:,1],q2[:,2]),
              w[1](q2[:,0],q2[:,1],q2[:,2]),
              w[2](q2[:,0],q2[:,1],q2[:,2])])
  mlab.close(all=True)
  nq=q2.shape[0]
  mlab.figure(1)
  mlab4sim.quiver(q2,me2,W,line_width=1,mask_points=nq//1000)
  mlab4sim.plotmesh(q1,me1,color='black',line_width=2)
  mlab.vectorbar()
  mlab.figure(2)
  mlab4sim.quiver(q2,me2,W,scalars=u, line_width=1,mask_points=nq//1000)
  mlab4sim.plotmesh(q1,me1,color='black',line_width=2)
  mlab.scalarbar()
  
def iso_surface3D01():
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u=f(q3[:,0],q3[:,1],q3[:,2])
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.iso_surface(q3,me3,u,contours=5)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  mlab.figure(2)
  mlab4sim.iso_surface(q3,me3,u,contours=np.linspace(-0.8,0.8,10))
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  
def streamline3D01(N=15):
  q3,me3=getMesh3D(3)
  q2,me2=getMesh3D(2)
  q1,me1=getMesh3D(1)
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  u=f(q3[:,0],q3[:,1],q3[:,2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([w[0](q3[:,0],q3[:,1],q3[:,2]),
              w[1](q3[:,0],q3[:,1],q3[:,2]),
              w[2](q3[:,0],q3[:,1],q3[:,2])])
  
  mlab.close(all=True) 
  mlab.figure(1)
  mlab4sim.streamline(q3,me3,u,W)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  mlab.figure(2)
  s_options={'visible':True}
  sw_options={'normal':(0,0,1),'resolution':6}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seedtype='plane',linetype='tube',
                   seed_options=s_options,
                   seed_widget_options=sw_options,
                   streamtracer_options=st_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()

  mlab.figure(3)
  sw_options={'center':(0.9,0,1), 'radius':0.1,'phi_resolution':8,
              'theta_resolution':12,'enabled':False}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  sw_options['center']=(0,0,1)
  sw_options['radius']=0.3
  mlab4sim.streamline(q3,me3,u,W,seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)

  mlab.figure(4)
  sw_options={'origin':(0,-1,0),'point1':(0,-1,2),'point2':(0,1,0),
              'enabled':True,'resolution':6}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seedtype='plane',
                   seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)  