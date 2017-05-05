import matplotlib as mpl
mpl.use("Agg")
import os
import errno
import contextlib, errno, os, time
import dwell.rad.terminal as terminal
import logging
from . import t15
from . import plots
from . import variables
from argh import arg
from collections import OrderedDict, defaultdict
import asciitable
import numpy 
import netCDF4 
import json
import pylab as pl
import seaborn as sns
sns.set_style("whitegrid")
from cycler import cycler
import pandas as pd

__program__ = "postprocess_plots"

def netCDF4_Dataset(fname):
    print(fname)
    return netCDF4.Dataset(fname)
defaults=dict(  t15_output_filename="t15_out.png",
                viking_output_filename="viking_out.png",
                testsk_output_filename="testsk_out.png"
            )

def load_defaults():
    filename = ".wrf_plots_defaults"
    paths=[".",os.path.expanduser("~")]

    for p in paths:
        fullpath=os.path.join(p,filename)
        if os.path.exists(fullpath):
            up = load_json(fullpath)
            defaults.update(up)



def load_json(filename):
    if isinstance(filename,list):
        d=dict()
        for f in filename:
            d.update(load_json(f))
        return d
    else: 
        return json.load(open(filename,'r'))

def csv(s):
    return s.split(",")

def csvf(s):
    return [float(f) for f in csv(s)]

def csvl(s):
    r=[]
    for e in csv(s):
        if e.count(":") == 1:
            l,h = [float(f) for f in e.split(":")]
            r.extend(list(range(l,h)))
        elif e.count(":") == 2:
            l,h,s = [float(f) for f in e.split(":")]
            r.extend(list(numpy.arange(l,h,s)))
        else:
            r.append(float(e))
    return r

def get_keynames(data,key,fuzzy=False):
    kd=[]
    for k in key:
        if k in data:
            kd.extend([k])
        elif fuzzy:
            kd.extend([j for j in data.keys() if j.count(k)])

    for k in kd:
        yield k
        
def get_filename(data,key, name):
    if isinstance(name,list):
        x=None
        for n in name:
            x=get_filename(data,key,n)
            if x is not None:
                return x
        return x
    if name in data[key]:
        return os.path.join(data[key]["directory"],data[key][name])
#    elif "default" in data[key]:
#        return os.path.join(data[key]["directory"],data[key]["default"])
    else:
        return None


def t0p5hpa_calc(fname, latitude, plev,variable,suffix):
    ls, t0p5hpa,p,pb = get_data(fname,"{0}{1}".format(variable,suffix),"L_s",
                                extra=["P{0}".format(suffix),"PB{0}".format(suffix)] )

    data = numpy.zeros(p.shape[0])
    data2 = numpy.zeros_like(data)
    for lat in latitude:
        if t0p5hpa.ndim > 2:
            p05 = p[:,:,lat] + pb[:,:,lat]
            t05 = t0p5hpa[:,:,lat]
    
            #hydrostatic altitude
            g=3.727
            rd=188.
    
            def gauss(x,mu,fwhm):
                sigma = fwhm/(2*numpy.sqrt(2*numpy.log(2.)))
                gweight = 1./(sigma*numpy.sqrt(2*numpy.pi)) * numpy.exp(-(x-mu)**2/(2.*sigma**2))
                return gweight/sum(gweight)
    
    
    
            for i in range(data.size):
                pval,tval= p05[i], t05[i]
                dlp = numpy.hstack([-0,numpy.diff(numpy.log(pval))])
                zval = numpy.cumsum(-dlp*rd*tval/g)/1.e3        
                zmu = numpy.interp(plev, pval[::-1],zval[::-1])
                data[i] += (1./len(latitude)) * numpy.interp(plev,pval[::-1],tval[::-1])
                data2[i] += (1./len(latitude)) * sum(gauss(zval,zmu,20.)*tval)
        else:
            data += (1./len(latitude)) * t0p5hpa[:,lat]
            data2 += (1./len(latitude)) * t0p5hpa[:,lat]
    return ls, data,data2

@arg("--input_names",type=csv)
@arg("json_filenames",nargs="+")
@arg("--xlim",type=csvf)
@arg("--ylim",type=csvf)
@arg("--latitude",type=csvf)
@arg("--filename_template","-f",type=str)
def t0p5hpa(json_filenames,output_filename=None, filename_template="zm_ampm",
    input_names=None,
    variable="T_PHY",
    am="_AM", 
    plev=50.,latitude=None,
    xlim=None,ylim=None,
            observations=None,obsvar=None,ylabel=None,fuzzy=False):
    latitude=latitude or [17,18]
    jsondata = load_json(json_filenames)
    input_names = input_names or list(jsondata.keys())
    m=plots.Tableau_10.get_mpl_colormap(N=10)
    pl.gca().set_prop_cycle(cycler('color',[m(i) for i in range(10)]))
    for count,name in enumerate(get_keynames(jsondata,input_names,fuzzy=fuzzy)):        
        fname = get_filename(jsondata, name, filename_template)
        suffix=am
        if fname:
            ls, data,data2 = t0p5hpa_calc(fname, latitude, plev, variable, suffix)
            plots.ls_plot(ls,data,alpha=0.1,label="interpolated {0}".format(name))
            plots.ls_plot(ls,data2,alpha=0.9,label=name)

    if observations and obsvar:
        ls, t05 = get_data(observations,obsvar,"L_s")
        if t05.ndim > 1:
            tobs = numpy.zeros(t05.shape[0])
            for lat in latitude:
                tobs = t05[:,lat] * 1./len(latitude)
        else:
            tobs=t05
        pl.plot(ls,tobs,label='obs')
#        pl.plot(ls+numpy.floor(ls.max()/360.)*360.,t05,label='obs')
    if ylabel:
        pl.gca().set_ylabel(ylabel)
    pl.legend(loc="upper right",framealpha=0.5)
    if xlim:
        pl.xlim(xlim)
    if ylim:
        pl.ylim(ylim)
    output_filename = output_filename or "t05.png"

    pl.savefig(output_filename)

@arg("--input_names",type=csv)
@arg("json_filenames",nargs="+")
def t15(json_filenames,output_filename=None, input_names=None,fuzzy=False):
    jsondata = load_json(json_filenames)
    input_names = input_names or list(jsondata.keys())
    for count,name in enumerate(get_keynames(jsondata,input_names,fuzzy=fuzzy)):        
        fname = get_filename(jsondata, name, ["t15","default"])
        if fname:
            try:
                data = asciitable.read(fname)
                plots.ls_plot(data["ls"],data["t15"],alpha=0.5,label=name)
            except Exception as e:
                print(e)
                print(fname)
                with pd.HDFStore(fname) as data:
                    plots.ls_plot(data['df']["ls"],data['df']["t15"],alpha=0.5,label=name)

        
    pl.gca().set_ylabel("T15 (K)")
    pl.legend(loc="upper right",framealpha=0.5)

    output_filename = output_filename or defaults["t15_output_filename"]

    pl.savefig(output_filename)

@arg("--input_names",type=csv)
@arg("--xlim",type=csvf)
@arg("--ylim",type=csvf)
@arg("json_filenames",nargs="+")
def lander(json_filenames,output_filename=None, input_names=None,lander='vl1',ylim=None,xlim=None,fuzzy=False):
    jsondata = load_json(json_filenames)
    input_names = input_names or list(jsondata.keys())
    m=plots.Tableau_10.get_mpl_colormap(N=10)
    pl.gca().set_prop_cycle(cycler('color',[m(i) for i in range(10)]))
    for count,name in enumerate(get_keynames(jsondata,input_names,fuzzy=fuzzy)):
        fname = get_filename(jsondata, name, [lander,"lander","default"])
        if fname:
            print(fname)
            ls, data = get_data(fname, lander, "L_s")
            plots.ls_plot(ls,data,alpha=0.5,label=name)
            
    if ylim:
        pl.ylim(ylim)
    if xlim:
        pl.xlim(xlim)
        
    pl.gca().set_ylabel("{0}".format(lander))
    pl.legend(loc="upper right",framealpha=0.5)

    output_filename = output_filename or defaults["viking_output_filename"]

    pl.savefig(output_filename)


def get_data(fname, variable, ls="L_s",extra=None):
    #print(fname, variable, ls)
    extradata=[]
    if fname.endswith(".nc") or fname.endswith(".nc4"):
        with netCDF4_Dataset(fname) as nc:
            lsdata = nc[ls][:]
            data = nc[variable][:]
            if extra is not None:
                extradata = [nc[e][:] for e in extra]
    elif fname.endswith("h5"):
        with pd.HDFStore(fname) as d:
            filedata = d['df']
            if ls in filedata:
                lsdata = filedata[ls][:]
            else:
                lsdata = filedata["ls"][:]
            data = filedata[variable].astype(float)
            if extra is not None:
                extradata = [nc[e][:] for e in extra]
    else:
        filedata = asciitable.read(fname)
        if ls in filedata.dtype.names:
            lsdata = filedata[ls][:]
        else:
            lsdata = filedata["ls"][:]
        data = filedata[variable][:]
        if extra is not None:
                extradata = [nc[e][:] for e in extra]

    r=[lsdata,data]
    if len(extradata):
        r.extend(extradata)
    return r

@arg("--input_names",type=csv)
@arg("--xlim",type=csvf)
@arg("--ylim",type=csvf)
@arg("json_filenames",nargs="+")
@arg("--filename_template","-f",type=str)
def zmplot(json_filenames,output_filename=None, input_names=None,variable='TSK_PM',filename_template="zm_ampm",latitude=16, xlim=None, ylim=None,level=0,fuzzy=False):
    jsondata = load_json(json_filenames)
    input_names = input_names or list(jsondata.keys())
    m=plots.Tableau_10.get_mpl_colormap(N=10)
    pl.gca().set_prop_cycle(cycler('color',[m(i) for i in range(10)]))
    for count,name in enumerate(get_keynames(jsondata,input_names,fuzzy=fuzzy)):
        fname = get_filename(jsondata, name, [variable,filename_template])
        if fname:
            print (fname)
            ls, data = get_data(fname, variable, ls="L_s")
            if data.ndim> 2:
                data = data[:,level,latitude]
            else: 
                data = data[:,latitude]
            plots.ls_plot(ls[:],data,alpha=0.5,label=name)
    pl.gca().set_ylabel(variable)
    pl.legend(loc="upper right",framealpha=0.5)
    if xlim:
        pl.xlim(xlim)
    if ylim:
        pl.ylim(ylim)
    output_filename = output_filename or "plot.png"

    pl.savefig(output_filename)


@arg("--input_names",type=csv)
@arg("--xlim",type=csvf)
@arg("--ylim",type=csvf)
@arg("--clevels",type=csvl)
@arg("json_filenames",nargs="+")
@arg("--filename_template","-f",type=str)
def zmcontour(json_filenames,output_extension=None, input_names=None,variable='TSK_PM',filename_template="zm_ampm",
        level=0, xlim=None, ylim=None,
        clevels=None):
    output_extension = output_extension or "png"
    jsondata = load_json(json_filenames)
    input_names = input_names or list(jsondata.keys())
    for count,name in enumerate(input_names):
        fname = get_filename(jsondata, name, filename_template)
        if fname:
            ls, data, xlat = get_data(fname, variable, "L_s", extra=["XLAT"])
            
            if data.ndim > 2:
                data = data[:,level,:]
            else:
                data=data[:]
            kwargs=dict(label=name,alpha=1.0)
            if clevels:
                kwargs["levels"] = clevels
            plots.xt_surface_plot(variables.continuous_ls(ls[:]),xlat,data,**kwargs)
            pl.gca().set_title(variable)

            if xlim:
                pl.xlim(xlim)
            if ylim:
                pl.ylim(ylim)
            output_filename = "contour.{0}.{1}.{2}".format(variable,name,output_extension)

            pl.savefig(output_filename)

@arg("json_filenames",nargs="+")
def list_models(json_filenames):
    jsondata = load_json(json_filenames)
    for k in jsondata:
        if "description" in jsondata[k]:
            print("{0}:{1} ".format(k,jsondata[k]["description"]))
        else:
            print (k)



def main():
    terminal.argh_main(__program__,[t15,list_models,lander,zmplot,zmcontour, t0p5hpa])


if __name__=="__main__":
    main()
