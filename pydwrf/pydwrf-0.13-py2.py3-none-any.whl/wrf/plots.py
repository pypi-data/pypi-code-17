from .wrf_exception import *
from . import nc
from . import variables
from . import analysis
import numpy as np
import matplotlib.cm as mpl_cm
import palettable.colorbrewer as cb
from pylab import contourf, plot, figure,gca
from palettable.colorbrewer.diverging import Spectral_11_r, RdBu_11_r
from palettable.colorbrewer.qualitative import Paired_11
from palettable.tableau import Tableau_10
from . import scaled_ticks as st

def get_map(cmap):
    """Get a color map based on the name
    """
    try:
        if isinstance(cmap,str):
            colormaps=dict(spectral=Spectral_11_r,
                           bluered=RdBu_11_r
                           )
            return colormaps[cmap]
        elif isinstance(cmap,list):
            return cb.get_map(*cmap)
        else:
            return Spectral_11_r
    except Exception as e:
        print("Colormap {0} failed: {1}".format(cmap,e))
        return Spectral_11_r

scale_dictionary=dict(tera=1e-12,giga=1e-9, mega=1e-6, kilo=1e-3,centi=1e2, micro=1e3, milli=1e6, nano=1e9, pico=1e12)

def convert_scale(scale):
    """
    return a scalar number based on the string and the dictionary in plots.py
    """
    if isinstance(scale,float) or isinstance(scale,int):
        return scale
    elif scale in scale_dictionary:
        return scale_dictionary[scale]
    else:
        raise WRF_Exception("Scale not found: {0}".format(scale))
        
    
def contourf_core(ax, x,y,z,cmap=None, scale=1.0, *args, **kwargs):
    """
        Core contourf function. 
        Args:
            ax (Axis) : The axis to plot on
            x: x data
            y: y data
            z: z data
            cmap: (optional) colormap
            scale: (optional) scale data by the scale factor

        Returns:
            contour object
    """
    colormap = get_map(cmap)
    sval=convert_scale(scale)
    if "levels" in kwargs:
        print(len(kwargs["levels"]))
        import matplotlib.colors as colors
        C=ax.contourf(x,y,sval*z,colormap.number, cmap=colormap.mpl_colormap,
                      norm=colors.BoundaryNorm(boundaries=kwargs["levels"],ncolors=256),*args, **kwargs)
    else:
        C=ax.contourf(x,y,sval*z,colormap.number, cmap=colormap.mpl_colormap, *args, **kwargs)
    return C

def plot_core(ax, x,y, scale=1.0, *args, **kwargs):
    """Core plot function. 
        Args:
            ax (Axis) : The axis to plot on
            x: x data
            y: y data
            scale: (optional) scale data by the scale factor

        Returns:
            plot object
    """
    sval = convert_scale(scale)
    P = ax.plot(x,y*sval, *args, **kwargs)
    return P

def ls_plot(x,y,loop=False,ylabel=None,cycle_colors=False, *args, **kwargs):
    """
        Plot against Ls and mark the x-axis appropriately
        Args:
            x: x data
            y: y data
            loop: (optional) True loops the data onto the same Ls range, False plots a continuous Ls
            ylab: (optional) y label
            cycle_colors: (optional) if True inhibits the changing of colors with each line from the same dataset
        Returns:
            plot object(s)
    """
    ax=gca()
    if not loop:
        xax = variables.continuous_ls(x)
        P=plot_core(ax,xax,y,*args, **kwargs)
    else:
        xax=x
        xs,ys = variables.split_ls(x,y)
        P=[]
        color=None
        incoming_color = 'color' in kwargs
        for i,xx in enumerate(zip(xs,ys)):
            if i>0 and not incoming_color and not cycle_colors:
                kwargs['color']=base_line.get_color()
                kwargs["label"]=None
            base_line, = plot_core(ax,xx[0],xx[1],*args, **kwargs)
            P.append(base_line)
        

    l,h=np.floor(xax.min()/90)*90, np.ceil((xax.max()+1)/90)*90
    t=np.arange(l,h+45,90)
    ax.set_xticks(t)
    ax.xaxis.set_major_formatter(st.LsFormatter())
    ax.set_xlabel("Ls")

    if ylabel is not None:
        ax.set_ylabel(ylabel)
    return P

def xt_surface_plot(x,y,z,*args, **kwargs):
    """
    Default surface plot with latitude and Ls ticks
        Args:
            x: x data, latitude
            y: y data, time
            z: z data
        Returns:
            figure/axis object
    """

    fig = figure(figsize=(5,6))
    ax=fig.gca()
    C=contourf_core(ax,x,y,z.T,*args, **kwargs)
    ax.set_ylim(-90,90)
    ax.set_yticks([-90,-45,0,45,90])
    l,h=np.floor(x.min()/90)*90, np.ceil((x.max()+1)/90)*90
    t=np.arange(l,h+45,90)
    ax.set_xticks(t)
    ax.xaxis.set_major_formatter(st.LsFormatter())
    ax.set_xlabel("Ls")
    ax.set_ylabel("Latitude")
    fig.colorbar(C, orientation='horizontal')         
    return fig

def yz_plot(x,y,z,surface_pressure=None,surface_pressure_y=None,cmap=None,*args, **kwargs):
    """
        Default latitude pressure plot with latitude and pressure axes
        Args:
            x: x data, latitude
            y: y data, pressure
            z: z data
            surface_pressure: (optional) surface pressure to mask data
            surface_pressure_y: (optional) y values for surface pressure, otherwise will use 'x' data
            scale: (optional) scale data by the scale factor

        Returns:
            None
    """
    colormap=get_map(cmap)
    fig = figure(figsize=(5,6))
    ax = fig.gca()
    C = ax.contourf(x,y,z,colormap.number, cmap=colormap.mpl_colormap, *args,**kwargs)
    if surface_pressure is not None:
        if surface_pressure_y is None:
            surface_pressure_y = x[0]
        ax.plot(surface_pressure_y,surface_pressure, color='black',lw=2)

    ax.set_ylim(y.max(),y.min())
    ax.set_yscale('log')
    ax.set_xlim(-90,90)
    ax.set_xticks([-90,-45,0,45,90])
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Pressure (Pa)")
    fig.colorbar(C, orientation='horizontal')         
    return fig

def tp_plot(x, y, z, surface_pressure=None, *args, **kwargs):
    """
        Default time pressure plot with latitude and pressure axes
        Args:
            x: x data, time
            y: y data, pressure
            z: z data
            surface_pressure: (optional) surface pressure to plot on figure
            scale: (optional) scale data by the scale factor

        Returns:
            figure/axis
    """
    fig = figure(figsize=(5,6))
    ax=fig.gca()
    C=contourf_core(ax, x,y,z,*args,**kwargs)
    if surface_pressure is not None:
        ax.plot(x[:,0],surface_pressure, color='black',lw=2)
    ax.set_ylim(y.max(),y.min())
    ax.set_yscale('log')
    
    l,h=np.floor(x.min()/90)*90, np.ceil((x.max()+1)/90)*90
    t=np.arange(l,h,90)
    ax.set_xticks(t)
    ax.xaxis.set_major_formatter(st.LsFormatter())

    ax.set_xlabel("Ls")
    ax.set_ylabel("Pressure (Pa)")
    fig.colorbar(C, orientation='horizontal')         
    return fig

def zonalmean_calendar(x,y,zz,surface_pressure=None, surface_pressure_y=None,cmap=None,*args, **kwargs):
    """plot a calendar of temperatures"""
    colormap=get_map(cmap)
    fig = figure(figsize=(8,11))
    for i,z in enumerate(zip(x,y,zz)):
        print(i)
        ax=subplot(4,3,i+1)
        C=ax.contourf(z[0],z[1],z[2],colormap.number, cmap=colormap.mpl_colormap, *args,**kwargs)
        if surface_pressure is not None:
            if surface_pressure_y is None:
                surface_pressure_y = x[0]
            ax.plot(surface_pressure_y[i],surface_pressure[i], color='black',lw=2)

            ax.set_ylim(z[1].max(),z[1].min())
            ax.set_yscale('log')
            ax.set_xlim(-90,90)
            ax.set_xticks([-90,-45,0,45,90])
            if i%3==0:
                ax.set_ylabel("Pressure (Pa)")
            if i>=9:
                ax.set_xlabel("Latitude")

def zonalmean_calendar_temp(infh,indices,cmap=None):
    """Take the zonal mean of temperature and plot 12 temperature plots"""
    temp,press,axis,surface,surface_pressure_y=[],[],[],[],[]
    for i,ind in enumerate(indices):
        t,p = variables.temperature(infh, ind, return_pressure=True)

        temp.append(analysis.zonalandtimemean(t))
        press.append(analysis.zonalandtimemean(p))
        surface.append(analysis.zonalandtimemean(variables.get(infh,"PSFC",ind)))
        axis.append(variables.coordinates(infh,"T",ind)[1][:,0]*np.ones(press[-1].shape))
        surface_pressure_y.append(variables.coordinates(infh,"PSFC",ind)[1])
                    
    zonalmean_calendar(axis,press,temp, surface_pressure=surface, surface_pressure_y=surface_pressure_y,cmap=cmap)
    
def zonalmean_temp(infh,indices=None,cmap=None):
    """
    Calculate the zonalmean temperature of a variable named in 'variable',  selecting time 'indices',
    selecting the latitude bins in 'latitude'
    """
    temp,press = variables.temperature(infh, indices, return_pressure=True)
    axis = variables.coordinates(infh, "T", indices)

    zm_temp = analysis.zonalandtimemean(temp)
    zm_press = analysis.zonalandtimemean(press)
    zm_surface_pressure = analysis.zonalandtimemean(variables.get(infh,"PSFC",indices))
    yz_plot(axis[1][:,0][None,:]*np.ones(zm_press.shape),zm_press, zm_temp, surface_pressure=zm_surface_pressure,cmap=cmap)
    
    return True

def zonalmean_variable(infh, variable, indices=None,cmap=None):
    """
    Calculate the zonal mean of a variable named in 'variable',  selecting time 'indices',
    selecting the latitude bins in 'latitude'
    """
    temp = variables.get(infh, variable, indices)
    axis = variables.coordinates(infh, variable, indices)
    press = variables.get(infh,"pressure",indices)
    zm_temp = analysis.zonalandtimemean(temp)
    zm_press = analysis.zonalandtimemean(press)
    zm_surface_pressure = analysis.zonalandtimemean(variables.get(infh,"PSFC",indices))
    axisp = variables.coordinates(infh, "PSFC", indices)
    fig = yz_plot(axis[1][:,0][None,:]*np.ones(zm_press.shape),zm_press, zm_temp, surface_pressure=zm_surface_pressure,
              surface_pressure_y = axisp[1][:,0],cmap=cmap)
    
    return fig

def zonalmean_surface_variable(infh,variable, indices=None,cmap=None):
    """
    Calculate the zonalmean of a surface variable named in 'variable', selecting time 'indices',
    selecting the latitude bins in 'latitude'
    """
    data = variables.get(infh, variable, indices)
    axis = variables.coordinates(infh,variable, indices)
    dz = analysis.zonalmean(data)
    ls = variables.get(infh, "L_S")[indices]
    xls = variables.axis_ls(infh,indices)
    fig = xt_surface_plot(xls,axis[1][:,0],dz,cmap=cmap)
    return fig

def zonalmean_time_variable(infh, variable, indices=None, latitude=None, cmap=None, *args, **kwargs):
    """
    Calculate the zonal and time mean of a variable named in 'variable',  selecting time 'indices',
    selecting the latitude bins in 'latitude'
    """
    data = variables.get(infh, variable, indices)
    axis = variables.coordinates(infh, variable, indices)
    press = variables.get(infh,"pressure",indices)
    zm_data = analysis.zonalmean(data[:,:,latitude,:])
    zm_press = analysis.zonalmean(press[:,:,latitude,:])

    xls = variables.axis_ls(infh, indices)

    zm_surface_pressure = analysis.zonalmean(variables.get(infh,"PSFC",indices)[:,latitude,:])
    axisp = variables.coordinates(infh, "PSFC", indices)
    fig = tp_plot(xls[:,None]*np.ones(zm_press.shape),zm_press, zm_data, surface_pressure=zm_surface_pressure, *args, **kwargs)
    
    return fig
