import logging
import astropy.io.ascii as asciitable
from collections import OrderedDict as odict
import numpy

class TESException(Exception):
    """Boring exception class to identify where the exception comes from"""
    def __init__(self, message):
        super(TESException,self).__init__(message)
        log = logging.getLogger("pydwrf")
        log.error(message)

def data_filename(modname, filename):
    """Given the module name, and filename, finds the path to the file from the python sys.modules
    dictionary. Used to access the header dictionary file"""
    
    import os, sys
    filename = os.path.join(
        os.path.dirname(sys.modules[modname].__file__),
        filename)
    return filename
    
def pressure_from_index(index):
    """Air temperatures are given on layers, this function returns a pressure value
    when given an index, starting from 1"""
    
    pressure_mbar = [   16.5815200, 12.9137000, 10.0572000, 7.8325550, 6.1000000, 
                        4.7506850, 3.6998370, 2.8814360, 2.2440650, 1.7476790, 
                        1.3610940, 1.0600210, 0.8255452, 0.6429352, 0.5007185, 
                        0.3899599, 0.3037011, 0.2365227, 0.1842040, 0.1434582, 
                        0.1117254, 0.0870000, 0.0678000, 0.0528000, 0.0411000, 
                        0.0320000, 0.0249000, 0.0194000, 0.0151000, 0.0118000, 
                        0.0091700, 0.0071400, 0.0055600, 0.0043300, 0.0033700, 
                        0.0026300, 0.0020500, 0.0015900]
                        

    return pressure_mbar[index-1]*1e2 #scale to pascal.
    
def type_convert(value, ty):
    """Converts a value use the 'ty' function. If ty is a string, assume
    it's the name of an element in the dictionary defined in format_function (e.g. int,float,str,double)"""
    
    if isinstance(ty, str):
        return format_function(ty)(value)
    else:
        return ty(value)

def format_function(string):
    """Given a string format name, return a function that converts to that format"""
    convert=dict(   str=str,
                    float=numpy.float32,
                    double=numpy.float64,
                    int=numpy.int32)
    convert[float]=numpy.float32
    convert[int]=numpy.int32
    convert[numpy.float32]=numpy.float32
    convert[numpy.float64]=numpy.float64
    convert[numpy.int32]=numpy.int32

    convert[str]=str
    return convert[string]

def default_missing(string):
    """Given a string format, return the default missing data value"""
    default=dict(   str="",
                    float=-9e36,
                    double=-9e36,
                    int=-2147483647)
    default[numpy.float32]=default["float"]
    default[numpy.float64]=default["double"]
    default[numpy.int32]=default["int"]
    default[str]=default["str"]
    return default[string]

def sanitize_header(hin, number=False):
    """removes square brackets and converts to lower case"""

    hout = hin
    bracketed_number = None
    if hout.count("."):
        hout = hout[hout.index(".")+1:]

    if hout.count("["):
        hout = hout[:hout.index("[")] #remove counter
        if number:
            bracketed_number = int(hin[1+hin.index("["):hin.index("]")])

    hout= hout.lower()
    if number:
        return hout, bracketed_number
    else:
        return hout
    
def generate_extra_axes(header):
    """Reads the header list and generates new axis for 
       them as integers only
        """
    found_header_arrays = dict()
    for headname_orig in header:
        headname, value = sanitize_header(headname_orig,number=True)
        if value:
            current_value = found_header_arrays.get(headname,list())
            current_value.append(value)
            found_header_arrays[headname] = current_value

    #I can't tell if this is high resolution data yet, so there's no point trying to 
    #convert e.g. radiance index to wavenumber
    #I will know this when constructing the observation, so I store the index number
    #for now, and wait until later to convert that to the real units.
    
    #If there are duplicate column names in the data, I generate a second dimension
    #even though I shouldn't. For safety, check for duplicates here (count>1) and
    #fake that dimension
    
    for headname in header:
        if header.count(headname) > 1:
            found_header_arrays[headname] = numpy.arange(header.count(headname))
    
    return found_header_arrays
        
def process_header(header):
    """Reads the header dictionary file, and creates a 
        new dictionary from the input header data"""
    log = logging.getLogger("pydwrf")
    header_filename = data_filename("pydwrf.tes","data/headers.txt")
    log.info("Reading {0}".format(header_filename))
    header_dictionary = asciitable.read(header_filename, delimiter=",", numpy=False)
    result = odict()
    sanitized_header=list()

    for headname_orig in header:
        headname = sanitize_header(headname_orig)
        #add the sanitized header to the list for pairing with data later
        sanitized_header.append(headname)
        
        #if the header is defined in the dictionary,
        #figure out how many times it appears (for array data, denoted by variable[N])
        #figure out it's type and missing data value form the header
        if headname in header_dictionary["name"]:
            index = header_dictionary["name"].index(headname)
            if headname in result:
                result[headname]["count"] = result[headname].get("count",0)+1
            else:
                result[headname]=dict([(x, header_dictionary[x][index]) for x in header_dictionary.keys()])
                result[headname]["count"] = 1

            #convert the type to a function
            result[headname]["type"] = format_function( result[headname]["type"])
            if result[headname]["missing_value"] == "none":
                #default value
                result[headname]["missing_value"] = default_missing(result[headname]["type"])
            result[headname]["missing_value"] =\
                    type_convert(result[headname]["missing_value"], result[headname]["type"])
        else:
            #needs to be defined in the dictionary, raise an error.
            errstring="Did not find {0} in dictionary".format(headname_orig)
            raise TESException(errstring)
    
    extra_axes = generate_extra_axes(header)
    #convert to a format that can be written to netcdf
    dimensions = odict(Time=None)
    variables_in = odict()
    
    #loop through header, create 'variable objects to write to file'
    for hk,hv in six.iteritems(result):
        variables_in[hk] = dict(type=hv["type"], 
                                dimensions=("Time",),
                                extra=dict())
        #if this data has more than one element per time, create a new dimension
        if hv["count"] > 1:
            dimname = "dim_{0}".format(hk)
#            dimensions[dimname] = hv["count"]
            variables_in[hk]["dimensions"] = ("Time",dimname,)
            #also generate the coordinate variable using the extra_axes data
            dimensions[dimname] = dict(type=int,
                                         dimensions=(dimname,),
                                         array=extra_axes.get(hk,numpy.arange(hv["count"]))) 
        if hv["missing_value"] != "none":
            variables_in[hk]["extra"]["fill_value"] = hv["missing_value"]
        else:
            variables_in[hk]["extra"]["fill_value"] = default_missing(variables_in["hk"]["type"])
            
    return dimensions,variables_in, result, sanitized_header
    
