import numpy as np
import mayavi 
from mayavi import mlab
import sys,os

from fc_tools.colors import str2rgb

def isMayavi():  
  ismayavi=True
  try:
    import tvtk
    import mayavi
  except ImportError:
    ismayavi=False
  return ismayavi


def find_Colors_and_legends(figs,prev_found):
  if not hasattr(figs, '__iter__'):
    if isinstance(figs,mayavi.core.module_manager.ModuleManager):
      prev_found.append(figs)
    elif hasattr(figs, 'children'):
      for ch in figs.children:
        prev_found=find_Colors_and_legends(ch,prev_found)
    return prev_found

  for f in figs:
    if isinstance(f,mayavi.core.module_manager.ModuleManager):
      prev_found.append(f)
    elif hasattr(f, 'children'):
      for ch in f.children:
        prev_found=find_Colors_and_legends(ch,prev_found)
  return prev_found

# get objects mayavi.core.lut_manager.LUTManager
def get_colorbars(**kwargs):
  enable=kwargs.pop('enable',None)
  figure=kwargs.pop('figure',None)
  if figure is None:
    F=find_Colors_and_legends(mlab.get_engine().scenes,[])
  else:
    assert(isinstance(figure,mayavi.core.scene.Scene)) # use mlab.figure(1)
    F=find_Colors_and_legends(figure,[])
  CBs=[]
  for f in F:
    slm=f.trait_get()['scalar_lut_manager']
    if enable is None:
      CBs.append(slm)
    elif slm.show_scalar_bar==enable:
      CBs.append(slm)
    slm=f.trait_get()['vector_lut_manager']
    if enable is None:
      CBs.append(slm)
    elif slm.show_scalar_bar==enable:
      CBs.append(slm)
  return CBs

# option='label_text_property' for example
def get_colorbars_option(option,**kwargs):
  CBs=get_colorbars(**kwargs)
  CBOs=[]
  for cb in CBs:
    CBOs.append(cb.trait_get()[option])
  return CBOs

def set_colorbars_option(option,**kwargs):
  CBs=get_colorbars(**kwargs)
  for cb in CBs:
    cbo=cb.trait_get()[option]
    cbo.trait_set(**kwargs)
    
# set_scenes(background=(1,1,1))
def set_scenes(**kwargs):
  for s in mlab.get_engine().scenes:
    s.scene.trait_set(**kwargs)

# set_colormap(mlab.figure(1),'viridis')
# set_colormap(mlab.figure(1),'jet')
def set_colormap(fig,cmap):
  CBs=get_colorbars(figure=fig)
  for cb in CBs:
    cb.lut_mode=cmap

###
 #'background_color': (0.0, 0.0, 0.0),
 #'background_opacity': 0.0,
 #'bold': 1,
 #'bold_': 1,
 #'class_name': 'vtkTextProperty',
 #'color': (1.0, 1.0, 1.0),
 #'debug': False,
 #'debug_': 0,
 #'font_family': 'arial',
 #'font_family_min_value': 0,
 #'font_file': None,
 #'font_size': 12,
 #'global_warning_display': 1,
 #'global_warning_display_': 1,
 #'italic': 1,
 #'italic_': 1,
 #'justification': 'left',
 #'line_offset': 0.0,
 #'line_spacing': 1.1,
 #'m_time': 1950933,
 #'opacity': 1.0,
 #'orientation': 0.0,
 #'reference_count': 2,
 #'shadow': 0,
 #'shadow_': 0,
 #'shadow_offset': array([ 1, -1]),
 #'vertical_justification': 'bottom'}
### 
def set_colorbar_text(CandLs,**kwargs):
  if not hasattr(CandLs, '__iter__'):
    if isinstance(CandLs,tvtk.tvtk_classes.text_property.TextProperty):
      CandL.trait_set(**kwargs)
  for cl in CandLs:
    set_colorbar_text(cl,**kwargs)
    
def vtk_SaveAllFigsAsFiles(filename,**kwargs):
  tag=kwargs.get('tag', False )
  figext=kwargs.get('format', 'png' )
  savedir=kwargs.get('dir', '.' )
  figs=kwargs.get('figs',None) # list of figures number
  verbose=kwargs.get('verbose',False)
  scale=kwargs.get('scale', 1.0 )
  if not isMayavi():
    print('Needs Mayavi ...')
    return
  from mayavi import mlab
  if tag:
    Softname='Python'
    V=sys.version.split(' ')[0]
    Release=V.replace('.','')
    Tag=Softname+Release
    # FullTag=Tag+'_Mayavi'+mayavi.__version__.replace('.','') 
    
  if not os.path.exists(savedir):
    os.makedirs(savedir)
  set_colorbars_option('label_text_property',color=(0,0,0)) 
  for i in range(len(figs)):
    nfig=figs[i]
    if tag:
      File=savedir+os.path.sep+filename+'_fig'+str(nfig)+'_'+Tag+'.'+figext
    else:
      File=savedir+os.path.sep+filename+'_fig'+str(nfig)+'.'+figext
                   
    fig=mlab.figure(nfig)
    old_bg=fig.scene.background
    fig.scene.background=(1, 1, 1)
    #old_fg=fig.scene.foreground
    #fig.scene.foreground=(0, 0, 0)
    if verbose:
      print('  Save Mayavi Scene %d in %s'%(nfig,File))
    mlab.savefig(File,magnification=scale) 
    fig.scene.background=old_bg
    #fig.scene.foreground=old_fg

def check_color(color):
  if color is None:
    return None
  if isinstance(color,tuple):
    return color
  if isinstance(color,str):
    rgb=str2rgb(color)
    
    return tuple(rgb)
  if isinstance(color,list) or isinstance(color,np.ndarray):
    return tuple(color)
  print("Unknow color :"+str(color) )
  return (0,0,0)  

