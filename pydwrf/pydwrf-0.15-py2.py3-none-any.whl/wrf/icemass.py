#!/usr/bin/env python
import matplotlib
import netCDF4
import dwell.rad.terminal as terminal
import numpy
from argh import arg
import astropy.io.ascii as asciitable
from collections import OrderedDict


def calculate_icemass(fname, rows=None):
    #do stuff here.
    nc = netCDF4.Dataset(fname)
    co2ice = nc.variables["CO2ICE"]
    if "XLAT_V" in nc.variables:
        dy = numpy.diff(nc.variables["XLAT_V"][:],axis=1)
    else:
        dy = numpy.mean(numpy.diff(nc.variables["XLAT"][:],axis=1))

    if "XLONG_U" in nc.variables:
        dx = numpy.diff(nc.variables["XLONG_U"][:],axis=2)
    else:
        dx = numpy.mean(numpy.diff(nc.variables["XLONG"][:],axis=2))

    y = nc.variables["XLAT"][:]
    d2r = numpy.deg2rad
    area = nc.RADIUS * nc.RADIUS * d2r(dx)*d2r(dy)*numpy.cos(d2r(y))

    ls = nc.variables["L_S"][:]
    times = ["".join(f) for f in nc.variables["Times"][:]]
    sl=slice(None)
    if isinstance(rows,list):
        sl=[]
        for t in rows:
            sl.append(times.index(t))

    ls=ls[sl]
    icemass = co2ice[sl]
    times = numpy.array(times)[sl]
    def areasum(ice,area):
        return numpy.ma.sum(numpy.ma.sum(ice*area,-1),-1)
    nh_icemass = areasum(icemass,numpy.ma.array(area,mask=y<0))
    sh_icemass = areasum(icemass,numpy.ma.array(area,mask=y>=0))
    icemass = areasum(icemass,area)
    total_area = areasum(1.0,area)
    return OrderedDict([("times",times),
                        ("ls",ls),
                        ("icemass",icemass),
                        ("nh_icemass",nh_icemass),
                        ("sh_icemass",sh_icemass)])

@arg("filenames",nargs="+")
def process(filenames, output=None):
    output = output or "icemass.data"
    data=[]
    for fname in filenames:
        print(fname)
        data.append(calculate_icemass(fname))
    if len(filenames) > 1:
        dic=OrderedDict()
        for k in ["ls","icemass","nh_icemass","sh_icemass"]:
            dic[k] = numpy.hstack(
                    list(zip([d[k] for d in data]))
                    )
        data = dic
    else:
        data = data[0] 
    print(list(data.keys()))
    with open(output,'w') as outhandle:
        asciitable.write(data,output=outhandle,delimiter=",",names=["ls","icemass","nh_icemass","sh_icemass"])
    return None

