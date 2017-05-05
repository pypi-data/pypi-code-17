import marstime
from argh import ArghParser, arg

def calculate(data_csv, input="ephemeris", output="msd"):
    """command line interface, specify comma separated ephemeris or msd"""
    
    data = [float(f) for f in data_csv.split(",")] 
    
    done=False
    if input.lower()=="ephemeris":
        if output.lower()=="msd":
            #convert ephemeris time to msd
            res = [convert_ephemeris_time_to_msd(t) for t in data]
            done=True
        elif output.lower()=="j2000_offset_utc":
            #convert ephemeris time to j2000_offset_utc
            res = [convert_ephemeris_time_to_j2000_offset_utc(t) for t in data]
            done=True
        elif output.lower()=="j2000_offset_tt":
            #convert ephemeris time to j2000_offset_tt
            res = [convert_ephemeris_time_to_j2000_offset_tt(t) for t in data]
            done=True
        elif output.lower()=="ls":
            #convert ephemeris time to j2000_offset_utc
            res = [convert_ephemeris_time_to_Ls(t) for t in data]
            done=True
    elif input.lower()=="msd":
        if output.lower()=="ephemeris":
            res = [convert_msd_to_ephemeris_time(m) for m in data]
            done=True
        elif output.lower()=="ls":
        #WHY
            res1 = [convert_msd_to_ephemeris_time(m) for m in data]
            res = [convert_ephemeris_time_to_Ls(t) for t in res1]
            done=True
    else:
        done=True
        
        
    if not done:
        print("Unknown conversion: {0}->{1}".format(input, output))
        import sys
        sys.exit(1)
    
    print("{0},{1}".format(input, output))
    for i,j in zip(data, res):
        print("{0},{1}".format(i,j))
    
    
def convert_ephemeris_time_to_j2000_offset_utc(time):
    """TES ephemeris time is given in reference to the J2000 epoch.
    The marstime package already works in reference to the J2000 epoch, so we have
    most of the tools already.
    """
    
    ephemeris_offset = 0 
    ephemeris_scale  = 1./86400.
    
    return time * ephemeris_scale + ephemeris_offset

def convert_ephemeris_time_to_j2000_offset_tt(time):
    """TES ephemeris time is given in reference to the J2000 epoch.
    The marstime package already works in reference to the J2000 epoch, so we have
    most of the tools already.
    """
    #calculate the offset in utc days
    j2000_offset_utc = convert_ephemeris_time_to_j2000_offset_utc(time)
    #convert to the absolute julian day
    j2000_utc = j2000_offset_utc + marstime.j2000_epoch()
    #calculate the offset in days and add it to make the terrestrial time version
    j2000_tt = marstime.julian_tt(j2000_utc)
    #remove the (same) offset from terrestrial time
    j2000_offset_tt = j2000_tt -  marstime.j2000_epoch()
    
    return j2000_offset_tt
    
def convert_ephemeris_time_to_msd(time):
    """TES ephemeris is seconds after J2000_utc, convert
    1. UTC seconds since J2000 to UTC days since J2000
    2. UTC days to TT days
    3. TT days to msd
    """
    j2000_ott = convert_ephemeris_time_to_j2000_offset_tt(time)
    
    msd = marstime.Mars_Solar_Date(j2000_ott)
    return msd
    
def convert_ephemeris_time_to_Ls(time):
    """Convert seconds since epoch to J2000_ott days and use to calculate Ls
    """
    j2000_ott = convert_ephemeris_time_to_j2000_offset_tt(time)
    ls = marstime.Mars_Ls(j2000_ott)
    return ls
    
def convert_msd_to_ephemeris_time(msd):
    """Convert MSD to J2000_tt days, then to J2000_utc days, the to ephemeris time"""
    
    j2000_utc = marstime.j2000_from_Mars_Solar_Date(msd)
    ephemeris_time = j2000_utc * 86400.
    return ephemeris_time
