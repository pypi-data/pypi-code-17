#Functions to deal with TES data.
from argh import ArghParser
import dwell.rad.log as mylog
import logging
import sys
from collections import OrderedDict
from . import tes_time
from . import processing
from .tes_core import TESException, process_header
from . import nc as netcdf
import numpy
#from tqdm import tqdm
import six

def binheader(binary, ascii):
    """
        Reads the header from the TES vanilla binary output

    Args:
        binary (string): Input filename that contains the binary header string
        ascii (string): if not None, contains the header name for each field

    Returns:
        tuple: formatting code for each column in the table, 
               names for each variable, or a list of names v{i=0..N}

    """
    #read the data format from the binary file
    input = open(binary,'rb')
    mask = input.readline()
    input.close()
    
    mask = [m for m in mask.strip()]

    #read the column names from an ascii file
    if ascii is not None:
        input = open(ascii,'r')
        header = input.readline()
        input.close()
        header=header.strip().split()
    else:
        header = ["v{0}".format(str(i)) for i in range(len(mask))]
    
    #convert the binary mask into numpy 
    def convert(a,b):
        d=dict(I=numpy.int64,U=numpy.uint64,R=numpy.float64)
        return str(a),d[b]

    read_format = [convert(i,m) for i,m in zip(header,mask)]
    input.close()

    return numpy.dtype(read_format), header

def read_chunk(input_data, buffer_size, data, mapper, sanitized_header_names, noprogressbar=False, binary=False, header_format=None):
    """
        Reads a chunk of data from the input_data, parses it as TES data and 
        returns a sanitized dictionary of data rows.
        
    Args:
        input_data (filehandle): The file to read
        buffer_size (string): if not None, contains the header name for each field

    Returns:
        tuple: formatting code for each column in the table, 
               names for each variable, or a list of names v{i=0..N}

    """
    """tries to read enough data to fill the buffer, returns the actual number read"""
    
    nlines = 0

        
    eof=False
    if binary:
        indata = numpy.fromfile(input_data, dtype=header_format, count=buffer_size)
        nlines = len(indata)
        for d in data:
                data[d]["curr"] = 0 #reset the counter
        for oldname,newname in zip(indata.dtype.names,sanitized_header_names):
            i=data[newname]["curr"]
            data[newname]["array"][:nlines,i] = indata[oldname]
            data[newname]["array"][nlines:,i] = data[newname]["missing_value"]
            data[newname]["curr"]=i+1
            if data[newname]["curr"] >  data[newname]["max"]:
                raise IndexError("Inconsistent internal data format {0} {1}".format(newname, data[newname]["curr"]))
        eof = nlines!=buffer_size 
        return data, nlines, eof
    else: #ascii
        if not noprogressbar:
            print("progressbar disabled")
            #pbar = tqdm(buffer_size)
            pass
        for line in input_data:
            if not line:
                eof=True
                break
            
            #fill the data_in variable with this row of data
            data_in = [m(v) for m,v in zip(mapper,line.split())] 
            #zero out the counters in the output data for this row
            for d in data:
                data[d]["curr"] = 0 #reset the counter
                
            #loop through the headers, placing the data in the right column
            for col, item in zip(sanitized_header_names, data_in): #pair the variables and column name  
                i=data[col]["curr"] #current counter value
                try:
                    data[col]["array"][nlines, i] = item #try storing the data
                except ValueError as e:
                    print("Could not convert item {0} value {1}".format(col,item)) #badly formatted, error
                    raise
                #track the position in the array to place the next data
                data[col]["curr"]=i+1 
                #if we maxed out, raise an error, should never happen
                if data[col]["curr"] >  data[col]["max"]:
                    raise IndexError("Inconsistent internal data format {0} {1}".format(col, data[col]["curr"]))
            #at this point we looped through 1 row
            nlines=nlines+1
            if not noprogressbar:
                pass
                #pbar.update(nlines)
            
            if nlines == buffer_size:
                break
    #here we are done reading a chunk of data
    return data, nlines,eof

def process_data(data, nlines_read, methods=None):
    """Processes the data buffer by adding in variables and/or aggregating"""
    if methods is None:
        methods = "add_variables,convert_longitude_from_TES_to_MOLA,aggregate_data"

    if methods != "":
        for m in methods.split(","):
            data, nlines_read = getattr(processing,m.strip())(data,nlines_read)
    
    return data, nlines_read
    
def vanilla(input=None, 
            prefix="default.nc", 
            ncformat="NETCDF4",
            buffer_size=100000,
            maxobs=10000000,
            max_obs_per_file = 1000,
            method=None,noprogressbar=False, header_filename=None, binary=False):
    """Given the start and end dates in Mars Solar dates, 
    call the vanilla command and parse the output to a NetCDF file"""

    log = logging.getLogger("pydwrf")
    header_format=None
    if input is None:
        #read from standard input
        input_data = sys.stdin
        if binary:
            input_data = open(input,'rb')
            input_data.readline() #waste the header
            header_format, header = binheader(input, header_filename)
        else:
            header = input_data.readline().split()
    else:
        if binary:
            input_data = open(input,'rb')
            input_data.readline() #waste the header
            header_format, header = binheader(input, header_filename)
        else:
            input_data = open(input,'r')
            header = input_data.readline().split()
            
    log.info("Starting")
    log.info("Reading Header Data")
    dimensions_in,variables_in, headers_in, sanitized_header_names = process_header(header)
    log.info("Creating NetCDF file")
    row=0
    data=dict()
    log.info("Defining buffer")
    
    for head, val in six.iteritems(headers_in):
        data[head] = variables_in[head]
        data[head].update(   dict( array=numpy.zeros((buffer_size,val["count"]), dtype=val["type"]),
                                    missing_value = data[head]["extra"]["fill_value"],
                                    max=val["count"],
                                    curr=0)
                         )

    #list of conversion functions
    mapper = [data[head]["type"] for head in sanitized_header_names]
    
    buffer_index=0
    big_line_counter = 0
    log.info("Starting loop")
    final_data = None
    n_obs_created = 0
    n_obs_created_this_file = 0
    #gives the maximum number of zeros in the counter
    mlog = 1+int ( numpy.ceil( numpy.log10 ( maxobs ) ) ) 
    if not noprogressbar:
        print("Progressbar will loop through multiple iterations, each consuming {0} lines".format(buffer_size))

    while True:
        log.debug("Reading Chunk: {0}".format(big_line_counter))
        incoming_data, nlines_read, eof = read_chunk(input_data, 
                                      buffer_size, 
                                      data, 
                                      mapper, 
                                      sanitized_header_names, noprogressbar=noprogressbar,
                                      binary=binary, header_format=header_format)
        
        #log.debug("Read {0} lines".format(nlines_read))
        if nlines_read > 0:
            big_line_counter += nlines_read
            outgoing_data, nlines_read = process_data(incoming_data, nlines_read, method)
            n_obs_created_this_file += nlines_read
            n_obs_created += nlines_read
            if final_data is None:
                final_data = outgoing_data
            else:
                for key in final_data:
                    final_data[key]["array"]=numpy.concatenate((final_data[key]["array"],outgoing_data[key]["array"]),axis=0)
            #log.debug("Lines : {0} {1}".format(nlines_read, big_line_counter))

        if nlines_read==0 or big_line_counter >= maxobs:
            eof=True
            
        #we have data from this round (nlines_read>0) and we've exceeded the max data, or run out of data (eof)
        if (nlines_read>0 and n_obs_created_this_file >= max_obs_per_file) or eof:
            #final data now stores the groups of outgoing data
            padded=format(big_line_counter,"0{0}d".format(mlog))
            filename = "{0}.{1}".format(prefix,padded)
            log.debug("Writing file {0} with {1} observations".format(filename, n_obs_created_this_file))
            final_data, nlines_written = netcdf.output_chunk(filename, ncformat, 
                                                    dimensions_in, final_data, 
                                                    n_obs_created_this_file,
                                                    big_line_counter)
            final_data = None
            n_obs_created_this_file = 0
            
        if eof:
            if nlines_read==0:
                log.info("No more data in file, {0} lines".format(big_line_counter))
            if big_line_counter >= maxobs:
                log.info("Maximum number of observed reached, {0} lines".format(big_line_counter))
            #we ran out of data
            break;

    log.info("Finished, {0} lines".format(big_line_counter))

def main():
    """Main function, sets up the log file, and calls the appropriate function to based on command line arguments"""
    parser = ArghParser()
    progname="pydwrf"
    parser = ArghParser()
    parser.add_argument("--very_verbose", action="store_true")
    mylog.command_line(parser, progname, default_verbosity="CRITICAL", default_file_verbosity="INFO")

    parser.add_commands([tes_time.calculate], namespace="time")
    parser.add_commands([vanilla])


    args = parser.parse_args()
    
    log = mylog.default_logger(progname,
                                    logfile=args.logfile,
                                    verbosity=args.verbosity, 
                                    file_verbosity=args.file_verbosity)
    log.info("Called as {0}".format(" ".join(sys.argv)))
    
    try:
        parser.dispatch()
        sys.exit(0)
    except Exception as e:
        log.error("Exception coming")
        log.error(e)
        if args.very_verbose:
            raise
        else:
            sys.exit(1)
    
