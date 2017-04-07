import numpy as np


class Utilities(object):
    """Utilities class"""

    list_of_time_units = ['s', 'ms', 'micros', 'ns']

    @staticmethod
    def convert_time_units(data=None, from_units='micros', to_units='s'):
        """convert the time units
        
        Parameters:
        * vdata: single data or array of value to convert
        * from_units: default 'micros'. Must be either ['s','micros','ns']
        * to_units: default 's'. Must be either ['s', 'micros', 'ns']
        
        """
        if data is None:
            raise ValueError("Please provide data to convert")

        list_of_time_units = Utilities.list_of_time_units
        if ( not (from_units in list_of_time_units) or
             not (to_units in list_of_time_units)):
            raise ValueError("Units convertion not supported")
    
        coeff = Utilities.get_time_conversion_coeff(from_units = from_units,
                                               to_units = to_units)
        
        if (type(data) is list):
            data = np.array(data)
        
        return data * coeff
    
    @staticmethod
    def get_time_conversion_coeff(from_units='micros', to_units='s'):
        """return the coefficient to use to convert from first units to second units
        
        Arguments:
        * from_units: default 'micros'. Must be in the list of list_of_time_units
        * to_units: default 's'. Must be in the list of list_of_time_units
        
        Returns:
        * coefficient to apply to data to convert from first units to second units provided
        
        Raises:
        * ValueError: if any of the units is not supported
        """

        if (not (from_units in Utilities.list_of_time_units) or
        not(to_units in Utilities.list_of_time_units)):
            raise ValueError("Units not supported")

        if from_units == to_units:
            return 1
        
        if from_units == 's':
            if to_units == 'ms': return 1.e3
            if to_units == 'micros': return 1.e6
            if to_units == 'ns': return 1.e9
            
        if from_units == 'ms':
            if to_units == 's': return 1.e-3
            if to_units == 'micros': return 1.e3
            if to_units == 'ns': return 1.e6

        if from_units == 'micros':
            if to_units == 's': return 1.e-6
            if to_units == 'ms': return 1.e-3
            if to_units == 'ns': return 1.e3

        if from_units == 'ns':
            if to_units == 's': return 1.e-9
            if to_units == 'ms': return 1.e-6
            if to_units == 'micros': return 1.e-3

    @staticmethod
    def array_multiply_coeff(data=None, coeff=1):
        """multiply each element of the array by the coeff
        
        Parameters:
        * data: array to apply coefficient on
        * coeff: default value is 1. Coefficient to apply
        
        Returns:
        * data * coefficient
        """
        if data is None:
            raise ValueError("Give me at least something to multiply!")
    
        final_data = np.array([])
        for _item in data:
            _value = float(_item) * float(coeff)
            final_data = np.append(final_data, _value)
            
        return final_data
    
    @staticmethod
    def array_add_coeff(data=None, coeff=1.):
        """Add coefficient to each element of the array
        
        Parameters:
        * data: array to apply coefficient on
        * coeff: default value is 1. Coefficient to apply
        
        Returns:
        * data + coefficient
        """
        if data is None:
            raise ValueError("Give ma at least something to add!")
        
        final_data = np.array([])
        for index in range(len(data)):
            _item = data[index]
            _value = _item + coeff
            final_data = np.append(final_data, _value)
            
        return final_data
           
    @staticmethod
    def array_divide_array(numerator=None, denominator=None):
        """Divide two arrays of the same size
        
        Parameters:
        * numerator: numpy array
        * denominator: numpy array
        
        Returns:
        * numerator / denominator
        
        Raises:
        * ValueError if array do not have the same size
        """
        if len(numerator) != len(denominator):
            raise ValueError("Arrays do not have the same size!")
        
        return numerator / denominator
            
    @staticmethod
    def array_minus_array(array1=None, array2=None):
        """Substract second array from first array provided
        
        Parameters:
        * array1: left side of the '-' operator
        * array2: right side of the '-' operator
        
        Returns:
        * Array1 - Array2
        
        Raises:
        * ValueError if arrays do not have the same size
        """
        if len(array1) != len(array2):
            raise ValueError("Arrays do not have the same size!")
        
        return array1 - array2
            
    @staticmethod
    def load_csv(filename=None):
        """Load a csv file and return its content
        
        Parameters:
        * filename: name of the csv file to load
        
        Returns:
        contents of the file as an array item for each line
        
        Raise:
        ValueError if format is wrong
        
        """
        _input_file = filename
        try:
            f = open(_input_file, 'r')
            _tof = []
            for _line in f:
                if '#' in _line:
                    continue
                _value = float(_line.strip())
                _tof.append(_value)
            return _tof
        except:
            raise ValueError("Bad file format")        
        
    @staticmethod
    def load_ascii(filename=None, sep=''):
        """Load an ascii file using the separator provided to separete the value in the same row
        
        Parameters:
        * filename: ascii full file name of file to load
        * sep: default ' '. Separator to use to separate values in the same row
        
        Returns:
        Array of values 
        
        Raise:
        ValueError if file does not exist or format is wrong
        """
        _input_file = filename
        try:
            _final_array = np.genfromtxt(_input_file, 
                                         delimiter = sep)
            return _final_array
        except:
            raise ValueError("Bad file format!")
        
    @staticmethod
    def save_csv(filename=None, metadata=None, data=None):
        """Create comma separated file (CSV)
        
        Arguments:
        * filename: name of output file
        * metadata: metadata string array (will be placed at the top of the file with '#' in front)
        * data: data float array"""
        sep = ", "
        f = open(filename, "w")
        for _meta in metadata:
            f.write("# " + _meta +  "\n")
        for _row in data:
            if (type(_row) is np.ndarray) or (type(_row) is list):
                _row_string = [str(x) for x in _row]
                _row_format = sep.join(_row_string)
            else:
                _row_format = str(_row)
            f.write(_row_format + "\n")
        f.close()        