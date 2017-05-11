import numpy as np
from mayavi import mlab

from fc_oogmsh import gmsh
from fc_simesh.siMesh import siMesh
from fc_simesh_mayavi.siMesh import plotmesh,plot,plotiso,slice,slicemesh,sliceiso,quiver,iso_surface,streamline

from fc_tools.colors import check_color

def plotmesh2D01(N=25):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh2d('condenser11',N)
  Th=siMesh(meshfile)
  mlab.figure(1)
  plotmesh(Th,legend=True)
  mlab.view(0,0)
  mlab.figure(2)
  plotmesh(Th,labels=[10,20],legend=True)
  plotmesh(Th,labels=[2,4,6,8],color='black',merge=True) # ,'Linestyle',':')
  mlab.view(0,0)
  mlab.figure(3)
  plotmesh(Th,color='LightGray',merge=True)
  plotmesh(Th,d=1,legend=True,line_width=2)
  mlab.view(0,0)
  mlab.figure(4)
  plotmesh(Th,color='LightGray')
  plotmesh(Th,d=1,legend=True,labels=[1,3,5,7,20,101,102,103,104])
  mlab.view(0,0)

def plotmesh3D01(N=10):
  meshfile=gmsh.buildmesh3d('cylinderkey',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  mlab.figure(1)
  plotmesh(Th,legend=True)
  plotmesh(Th,d=1,color='black',line_width=3,merge=True)
  mlab.figure(2)
  plotmesh(Th,d=2,legend=True,merge=True)
  mlab.figure(3)
  plotmesh(Th,d=2,labels=[1,1000,1020,1021], color='LightGray', opacity=0.1,merge=True)
  # plotmesh(Th,d=2,labels=[1000],color='black', bounds=True)  # To do
  plotmesh(Th,d=2,labels=[10,11,31,2000,2020,2021],legend=True)
  mlab.figure(4)
  plotmesh(Th,d=2,  color='LightGray', opacity=0.1,merge=True)
  plotmesh(Th,d=1,legend=True,line_width=3)
  mlab.figure(5)
  from fc_tools.graphics import Plane
  P=[Plane(origin=[0,0,1],normal=[0,0,-1]), Plane(origin=[0,0,1],normal=[0,-1,-1])] 
  plotmesh(Th,d=1,color='black',merge=True)
  plotmesh(Th,cut_planes=P,color='DarkGrey',merge=True)
  plotmesh(Th,d=2,cut_planes=P,legend=True)
  mlab.view(-146,67,6)
  mlab.figure(6)
  P=Plane(origin=[0,0,1],normal=[-1,0,0])
  plotmesh(Th,d=1,color='black',merge=True)
  plotmesh(Th,cut_planes=[P],color='DarkGrey',merge=True)
  plotmesh(Th,d=2,cut_planes=[P],legend=True)
  mlab.view(118,45,6)
  return Th
  
def plotmesh3Ds01(N=20):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3ds('demisphere5',20)
  Th=siMesh(meshfile)
  mlab.figure(1)
  plotmesh(Th,legend=True)
  mlab.figure(2)
  plotmesh(Th,color='LightGray',opacity=0.1,merge=True)
  plotmesh(Th,d=1,legend=True,line_width=2)
  mlab.figure(3)
  plotmesh(Th,labels=[1,10,13,12])
  vp=plotmesh(Th,labels=[11],representation='surface')
  vp[0].actor.property.edge_visibility=True
  mlab.figure(4)
  vp=plotmesh(Th,legend=True,labels=[10,13,12], representation='surface')
  for i in range(len(vp)):
    vp[i].actor.property.edge_visibility=True
    vp[i].actor.property.edge_color=check_color('LightGray')
  plotmesh(Th,labels=[1,11],color='LightGray',opacity=0.1,merge=True)
  return Th

def plot2D01(N=25):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh2d('condenser11',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y))
  mlab.figure(1)
  plot(Th,u,colormap='viridis')
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(2)
  plot(Th,u,labels=[10,20],colormap='viridis')
  vp=plot(Th,u,labels=[2,4,6,8],colormap='viridis')
  mlab.view(0,0)
  vp.actor.property.edge_visibility=True
  vp.actor.property.line_width=0.5
  mlab.figure(3)
  plot(Th,u,colormap='viridis',plane=False)
  mlab.colorbar()
  mlab.figure(4)
  plot(Th,u,labels=[10,20],colormap='viridis',plane=False)
  vp=plot(Th,u,labels=[2,4,6,8],colormap='viridis',plane=False,merge=False)
  for i in range(len(vp)):
    vp[i].actor.property.edge_visibility=True
    vp[i].actor.property.line_width=0.5
  mlab.figure(5)
  plot(Th,u,d=1,colormap='viridis',line_width=2)
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True)
  mlab.colorbar()
 
  mlab.figure(6)
  plot(Th,u,d=1,colormap='viridis',line_width=2,plane=False)
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True,z=u)
  mlab.colorbar()
  
  
  return Th
  
def plot3D01(N=15):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3d('cylinderkey',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  plot(Th,u,colormap='jet',line_width=0.5)
  mlab.colorbar()
  mlab.figure(2)
  #plotmesh(Th,d=2,labels=[1,1000,1020,1021], color='LightGray', opacity=0.1)
  plot(Th,u,d=2,labels=[2000,2020,2021])
  vp=plot(Th,u,d=2,labels=[31],representation='wireframe')
  vp.actor.property.lighting=False
  vp.actor.property.line_width=0.5
  vp=plot(Th,u,d=2,labels=[10,11],merge=False)
  for i in range(len(vp)):
    vp[i].actor.property.edge_visibility=True
    vp[i].actor.property.line_width=0.5
  plot(Th,u,d=1,labels=[1075,1077,1078,1081],line_width=3)
  mlab.colorbar()
  return Th
    
def plot3Ds01(N=30):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3ds('demisphere5',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  plot(Th,u,colormap='jet',line_width=0.5)
  mlab.colorbar()
  mlab.figure(2)
  #plotmesh(Th,d=2,labels=[1,1000,1020,1021], color='LightGray', opacity=0.1)
  plot(Th,u,labels=[10,12],opacity=0.5)
  vp=plot(Th,u,labels=[1,11],representation='wireframe',merge=False)
  for i in range(len(vp)):
    vp[i].actor.property.lighting=False
    vp[i].actor.property.line_width=0.5
  plot(Th,u,d=1,line_width=3)
  mlab.colorbar()
  return Th
    
def plotiso2D01(N=50):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh2d('condenser11',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y))
  mlab.figure(1)
  plotiso(Th,u,contours=25,colormap='viridis')
  plotmesh(Th,d=1,color='black',merge=True)
  plotmesh(Th,d=2,color='LightGray',representation='surface',opacity=0.4,merge=True)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(2)
  plotiso(Th,u,contours=np.arange(-1,1,0.1),labels=[10,20],colormap='viridis')
  plotmesh(Th,d=2,color='LightGray',representation='surface', opacity=0.4, labels=[10,20] ,merge=True)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(3)
  plotiso(Th,u,contours=15,colormap='viridis',labels=[2,4,6,8])
  plotmesh(Th,d=2,color='LightGray',representation='surface',opacity=0.4,labels=[2,4,6,8] ,merge=True)
  plotiso(Th,u,contours=15,color='white',labels=[10,20])
  plot(Th,u,labels=[10,20],colormap='viridis')
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(4)
  plotiso(Th,u,contours=15,colormap='viridis',labels=[2,4,6,8,20],plane=False)
  plot(Th,u,labels=[2,4,6,8,20],colormap='viridis',opacity=0.5,plane=False)
  plotiso(Th,u,contours=15,color='white',labels=[10],plane=False)
  plot(Th,u,labels=[10],colormap='viridis',plane=False)
  mlab.colorbar()
  mlab.view(-41,71,7)
  return Th
  
def plotiso3D01(N=15):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3d('cylinderkey',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  plot(Th,u,d=2,labels=[10,11,31],opacity=0.5)
  plotiso(Th,u,d=2,line_width=2)
  plotmesh(Th,d=2,labels=[1000,1020,1021,2000,2020,2021], color='LightGray', opacity=0.1, merge=True)
  mlab.colorbar()
  mlab.figure(2)
  plot(Th,u,d=2,labels=[10,11],opacity=0.5)
  plotmesh(Th,d=2,labels=[31,2000,2020,2021], color='LightGray', representation='surface', merge=True)
  plotiso(Th,u,d=2,labels=[10,11,31,2000,2020,2021], contours=15, line_width=2)
  mlab.colorbar()
  mlab.view(65,74,7)
  return Th

def plotiso3Ds01(N=30):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3ds('demisphere5',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  plot(Th,u, opacity=0.7)
  plotiso(Th,u, line_width=1.5)
  mlab.colorbar()
  mlab.figure(2)
  #plotmesh(Th,d=2,labels=[1,1000,1020,1021], color='LightGray', opacity=0.1)
  plot(Th,u,labels=[13])
  plotiso(Th,u, labels=[13], color='white', line_width=1.5)
  plot(Th,u,labels=[10,12],opacity=0.4)
  plotmesh(Th,labels=[1], representation='surface', color='LightGray')
  plotiso(Th,u, labels=[1,10,12], line_width=1.5)
  plotmesh(Th,d=1, color='black', line_width=1.5,merge=True)
  mlab.colorbar()
  return Th  

def slicemesh3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  mlab.figure(1)
  plotmesh(Th,legend=True)
  plotmesh(Th,d=1,color='black',line_width=3,merge=True)
  mlab.figure(2)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  slicemesh(Th,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.figure(3)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slicemesh(Th,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.figure(4)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slicemesh(Th,labels=[10,11],origin=(0,0,1),normal=normal, color='LightGray')
    slicemesh(Th,labels=[1],origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  return Th

def slice3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  slice(Th,u,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.colorbar()
  mlab.figure(2)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slice(Th,u,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  mlab.figure(3)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slice(Th,u,labels=[1],origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  mlab.figure(4)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for z in [0,0.5,1,1.5]:
    slice(Th,u,labels=[1],origin=(0,0,z),normal=(-1,0,1), opacity=0.6)
  mlab.view(110,71,7)
  mlab.colorbar()
  return Th

def sliceiso3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  mlab.figure(1)
  sliceiso(Th,u,origin=(0,0,1),normal=(-1,0,1), colormap='viridis')
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  slicemesh(Th,origin=(0,0,1),normal=(-1,0,1), color='Gray')
  mlab.colorbar()
  mlab.view(132,53,7)
  mlab.figure(2)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slicemesh(Th,origin=(0,0,1),normal=normal, color='LightGray')
    sliceiso(Th,u,contours=20,origin=(0,0,1),normal=normal, line_width=2)#, w_enabled=True)
  mlab.colorbar()
  mlab.view(155,66,7)
  mlab.figure(3)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    slicemesh(Th,origin=(0,0,1),normal=normal, color='LightGray')
    sliceiso(Th,u, contours=20, labels=[1],origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  mlab.figure(4)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  for z in [0,0.5,1,1.5]:
    slice(Th,u,labels=[1],origin=(0,0,z),normal=(-1,0,1) )
    sliceiso(Th,u,labels=[1],origin=(0,0,z),normal=(-1,0,1), color='white')
  mlab.colorbar()
  mlab.view(110,71,7)
  return Th

def quiver2D01(N=50):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh2d('condenser11',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y: 5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y))
  w=[lambda x,y: y*np.cos(-(x**2+y**2)/10), lambda x,y: -x*np.cos(-(x**2+y**2)/10)]
  W=np.array([Th.feval(w[0]),Th.feval(w[1])])
  mlab.figure(1)
  quiver(Th,W, scale_factor=0.05 ,line_width=1, mask_points=Th.nq//2000)
  plotmesh(Th,d=1,color='black',merge=True)
  mlab.vectorbar()
  mlab.view(0,0)
  mlab.figure(2)
  quiver(Th,W, scalars=u, scale_factor=0.05,line_width=1, mask_points=Th.nq//2000)
  plotmesh(Th,d=1,color='black',merge=True)
  mlab.scalarbar()
  mlab.view(0,0)
  mlab.figure(3)
  quiver(Th,W,labels=[2,4,6,8,20] , scale_factor=0.05 ,line_width=1, mask_points=Th.nq//2000)
  plotmesh(Th,d=1,color='black',merge=True)
  mlab.vectorbar()
  mlab.view(0,0)
  mlab.figure(4)
  quiver(Th,W,labels=[2,4,6,8,20], scalars=u, scale_factor=0.05,line_width=1, mask_points=Th.nq//2000)
  plotmesh(Th,d=1,color='black',merge=True)
  mlab.scalarbar()
  mlab.view(0,0)
  
  return Th

def quiver3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([Th.feval(w[0]),Th.feval(w[1]),Th.feval(w[2])])
  mlab.figure(1)
  quiver(Th,W,line_width=1, mask_points=Th.nq//3000)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.vectorbar()
  mlab.figure(3)
  quiver(Th,W,labels=[10,11],line_width=1, mask_points=Th.nq//3000)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.vectorbar()
  
  mlab.figure(2)
  quiver(Th,W,scalars=u, line_width=1, mask_points=Th.nq//3000)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.scalarbar()
  mlab.figure(4)
  quiver(Th,W,scalars=u, labels=[10,11],line_width=1, mask_points=Th.nq//3000)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.scalarbar()
  return Th

def quiver3Ds01(N=30):
  mlab.close(all=True) 
  meshfile=gmsh.buildmesh3ds('demisphere5',N)
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z]
  W=np.array([Th.feval(w[0]),Th.feval(w[1]),Th.feval(w[2])])
  
  mlab.figure(1)
  quiver(Th,W)
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True)
  plotmesh(Th,d=1,color='black',line_width=2,merge=True)
  mlab.vectorbar()
  
  mlab.figure(2)
  quiver(Th,W,labels=[1,10,12])
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True)
  plotmesh(Th,d=1,color='black',line_width=2,merge=True)
  mlab.vectorbar()
  
  mlab.figure(3)
  quiver(Th,W,scalars=u)
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True)
  plotmesh(Th,d=1,color='black',line_width=2,merge=True)
  mlab.scalarbar()
  
  mlab.figure(4)
  quiver(Th,W,scalars=u,labels=[1,10,12])
  plotmesh(Th,color='LightGray',opacity=0.05,merge=True)
  plotmesh(Th,d=1,color='black',line_width=2,merge=True)
  mlab.scalarbar()
  return Th  

def isosurface3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  u=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([Th.feval(w[0]),Th.feval(w[1]),Th.feval(w[2])])
  mlab.figure(1)
  iso_surface(Th,u,contours=10)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.colorbar()
  mlab.figure(2)
  iso_surface(Th,u,labels=[10,11],contours=10)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.colorbar()
  return Th

def streamline3D01(N=15):
  meshfile=gmsh.buildmesh3d('cylinder3dom',N)
  mlab.close(all=True) 
  Th=siMesh(meshfile)
  U=Th.feval(lambda x,y,z: 3*x**2-y**3+z**2+x*y)
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([Th.feval(w[0]),Th.feval(w[1]),Th.feval(w[2])])
  mlab.figure(1)
  streamline(Th,U,W)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.colorbar()
  mlab.figure(2)
  s_options={'visible':True}
  sw_options={'normal':(0,0,1),'resolution':6}
  st_options={'integration_direction':'both'}
  sl=streamline(Th,U,W,seedtype='plane',linetype='tube',
                       seed_options=s_options,
                       seed_widget_options=sw_options,
                       streamtracer_options=st_options)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)
  mlab.colorbar()

  mlab.figure(3)
  sw_options={'center':(0.9,0,1), 'radius':0.1,'phi_resolution':8,
              'theta_resolution':12,'enabled':False}
  st_options={'integration_direction':'both'}
  sl1=streamline(Th,U,W,seed_widget_options=sw_options,
                        streamtracer_options=st_options,colormap='jet')
  sw_options['center']=(0,0,1)
  sw_options['radius']=0.3
  sl2=streamline(Th,U,W,seed_widget_options=sw_options,
                        streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)

  mlab.figure(4)
  sw_options={'origin':(0,-1,0),'point1':(0,-1,2),'point2':(0,1,0),
              'enabled':True,'resolution':6}
  st_options={'integration_direction':'both'}
  sl1=streamline(Th,U,W,seedtype='plane',
                        seed_widget_options=sw_options,
                        streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  plotmesh(Th,d=2,color='LightGray',opacity=0.05,merge=True)  
  return Th