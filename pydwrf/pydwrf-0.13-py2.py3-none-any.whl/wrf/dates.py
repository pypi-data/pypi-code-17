import bisect
import numpy

class times_wrapper(object):
    """Time wrapper class that allows getitem calls to return the full string"""
    def __init__(self,data,range=None):
        if range is None:
            range=slice(0,4,None)
        self.range=range
        self.data = data
        return
    def __getitem__(self,index):
        res=self.data[index,self.range]
        if res.ndim > 1:
            return numpy.array([int("".join(d)) for d in res])
        else:
            return numpy.array([int("".join(res))])
    def __len__(self):
        return len(self.data)

def parse_date(s):
    """parse the date into parts"""
    string="".join(s)
    return [int(i) for i in [string[0:4],string[5:10],string[11:13],string[14:16],string[17:19]]]

def find_year_range_in_file(times,low,high):
    """Reading strings from NetCDF files are horribly slow. 
    Using a wrapper class and bisect search to find the year boundarys.
    Assumes they are contiguous.
    """
    twrap = times_wrapper(times)#default to year wrapper
    low_index = bisect.bisect_left(twrap,low)
    high_index = bisect.bisect_right(twrap,high)
    return low_index, high_index
    

def get_year(string):
    """given a WRF times string, return the year in integer form"""
    return parse_date(string)[0]

def get_day(string):
    """given a WRF times string, return the day in integer form"""
    return parse_date(string)[1]

def get_hour(string):
    """Get the hours from the WRF date string"""
    return parse_date(string)[2]

def get_minute(string):
    """Get the minutes from the WRF date string"""
    return parse_date(string)[3]

def get_second(string):
    """Get the seconds from the WRF date string"""
    return parse_date(string)[4]

def date_to_dict(string):
    """Returns a dictionary of the parsed date"""
    return dict(zip(["year","hour","minute","second"],parse_date(string)))


    
    
