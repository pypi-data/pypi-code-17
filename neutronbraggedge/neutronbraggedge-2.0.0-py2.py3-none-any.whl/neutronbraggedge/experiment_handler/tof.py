import numpy as np
import os
from ..utilities import Utilities


class TOF(object):
    """This class handles the loading of the TOF and the automatic conversion to 's'"""
    
    tof_array = []
    counts_array = []
    
    def __init__(self, filename=None, tof_array=None, units='s'):
        """Constructor of the TOF class
        
        Arguments:
        * filename: optional input file name. If file exist, data will be automatically loaded 
        (only CSV file is supported so far)
           example: file_tof.txt
                    #first row of the file
                    1.0  34
                    2.2  31
                    3.4  5
                    4.5  10
                    5.6  22
                    ...

        * tof_array: optional tof array. This argument will be ignored if filename is not None
        * units: optional units of the input tof array (default to 'seconds')

        Raises:
        * ValueError: - input file provided as the wrong format
                      - neither input file and tof_array are provided
                      
        * IOError: - file does not exist
        
        """

        if (filename is not None):
            if os.path.isfile(filename):
                self.filename = filename
                self.load_data()
            else:
                raise IOError("File does not exist")
        else:
            if (tof_array is not None):
                if (not type(tof_array) is np.ndarray):
                    self.tof_array = np.array(tof_array)
                else:
                    self.tof_array = tof_array
            else:
                raise ValueError("Please provide a tof array")

        if units is not 's':
            self.tof_array = Utilities.convert_time_units(data = self.tof_array,
                                                    from_units = units,
                                                    to_units = 's')
        
        
    def load_data(self):
        """Load the data from the filename name provided"""
        
        # only loader implemented so far !
        _ascii_array = Utilities.load_ascii(filename = self.filename, sep='')
        _tof_column = _ascii_array[:,0]
        self.tof_array = _tof_column

        _counts_column = _ascii_array[:,1]
        self.counts_array = _counts_column
        

