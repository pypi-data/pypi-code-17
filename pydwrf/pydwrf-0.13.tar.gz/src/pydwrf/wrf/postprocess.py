"""Postprocessing code for WRF data"""
import os
import errno
import contextlib, errno, os, time
import dwell.rad.terminal as terminal
import logging
from . import t15
from argh import arg
from collections import OrderedDict, defaultdict
import asciitable
import numpy 
import netCDF4 
from glob import glob
import json
import pandas as pd

__program__ = "postprocess"

@contextlib.contextmanager
def flock(path, wait_delay=.1):
    """ File Locking for wrfout files"""
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            time.sleep(wait_delay)
            continue
        else:
            break
    try:
        yield fd
    finally:
        os.close(fd)
        os.unlink(path)

def make_sure_path_exists(path):
    """Check for path, else make the directory"""
    if path=="":
        return
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def make_sure_path_exists_for_filename(filename):
    """"Given a filename, make sure the directory exists, else make it"""
    dirname = os.path.dirname(filename)
    make_sure_path_exists(dirname)


def netcdf3to4(filename,output_filename=None):
    """ Convert netcdf 3 to 4 using the nccopy program"""
    log = logging.getLogger(__program__)
    log.debug("netcdf3to4 filename : {0}".format(filename))


    from subprocess import call
    with flock("{0}.lock".format(filename)):
        if output_filename is None: 
            output_filename="{0}.nc4".format(filename)
            log.debug("output_filename : {0}".format(output_filename))
        call(["nccopy","-u","-7",filename, output_filename])

def read_output_data(filename):
    """Read the filename in H5, ascii, or plain text format.

        Args:
            filename: filename
        Returns:
            table of data
    """
    log=logging.getLogger(__program__)
    name,ext = os.path.splitext(filename)
    if not os.path.exists(filename):
        data = pd.DataFrame({"times":[]})
        data = data.set_index("times")
        return data
    if ext == ".h5":
        from . import h5
        print("h5")
        data = h5.read(filename)
    elif ext == ".ascii":
        from . import ascii
        print("ascii")
        data = pd.read_table(filename,delimiter=',',index_col=0)
    else:
        data = pd.read_table(filename,delimiter=',',index_col=0)
    return data

def output_data(filename, data,keys):
    """write the filename in H5, ascii, or plain text format.
        
        Args:
            filename: filename
            data: table data
            keys: keys to write
        Returns:
            None
    """
    log=logging.getLogger(__program__)
    name, ext = os.path.splitext(filename)
    if ext == ".h5":
        from . import h5
        print("h5")
        h5.write(filename,data,keys,log=log)
    elif ext == ".ascii":
        from . import ascii
        if len(data.index): #assume it's a Pandas table
            data.to_csv(filename)
        else:
            data.set_index('times').to_csv(filename)
    else: #single file, no updates.
        with open(filename,'w') as outhandle:
            asciitable.write(data,output=outhandle,delimiter=",")

def find_unprocessed(data,times,target):

    valid_times=[]
    index=[]
    
    if target not in list(data.columns.values):
        valid_times = times
        index=slice(None)
    else:
        for i,t in enumerate(times):
            if t not in data.index:
                valid_times.append(t)
            else: #row is there, check it
                if numpy.isnan(data[target][t]):
                    valid_times.append(t)
                    index.append(i)
    return valid_times, index

@arg("filenames", nargs="*")
def calculate_t15(filenames,output=None,interpolate_obs=False):
    """Program to calculate T15 brightness temperatures
        
        Args:
            filename: filename
        Returns:
            table of data
    """
    output=output or "model.data"
    log = logging.getLogger(__program__)
    data = read_output_data(output)        
    updated_file=False
    if filenames is None or len(filenames)==0: 
        filenames = sorted(glob("wrfo*"))
        
    for fname in filenames:
        log.info("T15 filename: {0}".format(fname))
        with netCDF4.Dataset(fname) as nc:
            times = ["".join(f) for f in nc.variables["Times"][:]] #all the times
        #look for unprocessed indices in this file
        valid_times, index = find_unprocessed(data,times,target)

        print("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),fname))
        log.info("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),fname))
        if len(valid_times):
            updated_file=True
            #calculate the index list from the fname
            dt=t15.process_file(fname,index)
            dd=dict(times=valid_times)
            dd.update(dt)
            if interpolate_obs:
                t15_ls,t15_t = t15.t15data()
                interp_t15_t = numpy.interp(dd["ls"],t15_ls,t15_t)
                dd["t15obs"]=interp_t15_t
        
            newdata = pd.DataFrame(dd)
            newdata.set_index("times",inplace=True)
            #merge table (assuming Pandas)
            data = merge_tables(data,newdata)
    #if the file was updated, write the new file
    if updated_file:
        output_data(output,data,[])
    return None


def merge_tables(data,newdata):
    """Merge data and newdata with a merge that replaces old data with new
        Args:
            data: old data
            newdata: new data
        Returns:
            merged data
    """
    newer_data = pd.concat([data,newdata],axis=0)
    newer_data = newer_data.groupby(newer_data.index).last() #reindex and replace old with new
    return newer_data
    
@arg("filenames", nargs="*")
def Ls(filenames,output=None,interpolate_obs=False):
    """Program to write the Ls data to the output file
        Args:
            filenames: wrfout files to process
            output: (optional) output filename. defaults to 'model.data'
        Returns:
            None
        Output:
            Ls and Times data in output file
    """
    output=output or "model.data"
    data = read_output_data(output)        
    log = logging.getLogger(__program__)
    #loop through filenames
    for filename in filenames:
        log.info(filename)
        newdata=dict(ls=[],times=[])
        with netCDF4.Dataset(filename) as nc:
            ls=nc["L_S"][:]
            times = ["".join(f) for f in nc.variables["Times"][:]]
            newdata = pd.DataFrame(dict(ls=ls,times=times))
            newdata.set_index("times",inplace=True)
            data = merge_tables(data,newdata)
    #save output data
    output_data(output,data,["ls"])

@arg("filenames", nargs="*")
def icemass(filenames,output=None,interpolate_obs=False):
    """Program to write the ice mass data to the output file
        Args:
            filenames: wrfout files to process
            output: (optional) output filename. defaults to 'model.data'
            interpolate_data: (optional) if True, add observational data to the output file
        Returns:
            None
        Output:
            Ls and Times data in output file
    """
    output=output or "model.data"
    data = read_output_data(output)
    log = logging.getLogger(__program__)
    from . import icemass
    updated_file=False
    for filename in filenames:
        nc = netCDF4.Dataset(filename)
        times = ["".join(f) for f in nc.variables["Times"][:]] #all the times
        nc.close()
        update = [False]*len(times)
        li=list(data.columns.values)
        valid_times, index = find_unprocessed(data,times,"icemass")
        print("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),filename))
        log.info("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),filename))
        if valid_times:
            updated_file=True
            dd=icemass.calculate_icemass(filename,valid_times)
            newdata = pd.DataFrame(dd)
            newdata.set_index('times',inplace=True)
            data = merge_tables(data,newdata)
        
    if updated_file:
        output_data(output,data,[])
    
def csvgen(f):
    #generate a cvs parse with a type conversion to type f
    l=lambda x: map(f,x.split(","))
    return l

@arg("filenames", nargs="*")
@arg("--lander",type=csvgen(str))
def lander(filenames, output=None, lander=None):
    """Program to write the ice mass data to the output file
        Args:
            filenames: wrfout files to process
            output: (optional) output filename. defaults to 'model.data'
            lander: (optional) select the lander from vl1,vl2,mpf,msl (comma separated list)
        Returns:
            None
        Output:
            Ls and Times data in output file
    """
    lander = lander or ["vl1"]
    output=output or "model.data"
    data = read_output_data(output)
    from . import vl
    functions=dict(vl1=vl.func_vl1_pressure_curve,
                   vl2=vl.func_vl2_pressure_curve,
                   mpf=vl.func_mpf_pressure_curve,
                   msl=vl.func_msl_pressure_curve)

    updated_file=False
    for l in lander:
        for filename in filenames:
            nc=netCDF4.Dataset(filename)
            times = ["".join(f) for f in nc.variables["Times"][:]]
            valid_times, index = find_unprocessed(data,times,l)
            print("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),filename))
            log.info("Processing {0} entries out of {1} for {2}".format(len(valid_times),len(times),filename))

            if len(valid_times):
                updated_file=True
                dd={"times":valid_times,l:functions[l](nc,index)}
                newdata = pd.DataFrame(dd)
                newdata.set_index("times",inplace=True)
                data = merge_tables(data,newdata)
            nc.close()

    if updated_file:
        output_data(output,data,[])
            

def dump_h5(filename,framename='df'):
    """Dump the H5 file to the terminal"""

    log = logging.getLogger(__program__)
    from . import h5
    with h5.pd.HDFStore(filename) as store:
        d=store[framename]
        asciitable.write(d, delimiter=',')
        
def process_directory(directory):
    """Process the directory for filenames.
        If the file being tested exists, store it's name in a dictionary

    """
    def storeifpresent(target,destination,dic,filelist):
        """Given a list of files, if the target is found
        store it's location in the dictionary under the destination key
        """
        if target in filelist:
            dic[destination] = target
        return dic
    
    files = glob("{0}/*".format(directory))
    
    dic=dict(directory=directory)
    dic["description"]=''
    dic.update(storeifpresent("wrfout.h5","default",dic,[os.path.basename(f) for f in files]))
    dic.update(storeifpresent("atm_zm.nc","zm",dic,[os.path.basename(f) for f in files]))
    dic.update(storeifpresent("atm_ampm_zm.nc","zm_ampm",dic,[os.path.basename(f) for f in files]))
    n=os.path.basename(os.path.dirname(directory if directory[-1] != "/" else directory[:-1]))
    return {n:dic}

def index(directory,name=None):
    """Index a directory by searching for relevant files,
    and output the resulting dictionary as a json encoded string"""

    d=process_directory(directory)
    if name is not None:
        k=d.keys()[0]
        d[name]=d[k]
        d.pop(k)
    print(json.dumps(d, indent=2))
    
def index_dirs(directory):
    """Index multiple directories.
    Look for subdirectories with a 'postprocessed' subdirectory, index and save each directory
    and output the json encoded string of all the directories.
    """
    subs = glob("{0}/*/postprocessed".format(directory))
    d=dict()
    for s in subs:
        n=os.path.basename(os.path.dirname(s))
        d.update(process_directory(s))
    print( json.dumps(d,indent=2))

@arg("json_files",nargs="+")
def index_merge(json_files):
    d=dict()
    for f in json_files:
        d.update(json.load(open(f)))
    print(
        )

def html_figures(inputdir, outputname):
    files = sorted(glob("{0}/*.png".format(inputdir)))
    mydir=os.getcwd()
    titlelist = ["<div><h2>{0}</h2>".format(f) for f in files]
    imglist = ["<img src=\"{0}\"></img></div>".format(f) for f in files]
    interleave = lambda x,y: [v for p in zip(x,y) for v in p]
    html="""
<html>
    <head>
        <style>
        div { float: left; }
        </style>
    </head>
"""+"""
    <body>
        <h1>{0}</h1>
          {1}
    </body>
</html>""".format(mydir,"".join(interleave(titlelist,imglist)))

    with open(outputname,'w') as out:
        out.write(html)

def main():
    terminal.argh_main(__program__,[netcdf3to4,
                                    calculate_t15,
                                    dump_h5,
                                    lander,
                                    icemass,
                                    Ls,
                                    index_dirs,
                                    index,
                                    index_merge,
                                    html_figures])


if __name__=="__main__":
    main()
