import numpy as np
import os
from ..utilities import Utilities


class LambdaWavelength(object):
    """This class handles the loading of the Lambda"""
    
    def __init__(self, filename=None, data=None):
        """Constructor of the LambdaWavelength class
        
        Arguments:
        * filename: optional input file name if data array is provided
        If file exist, data will be automatically loaded 
        (only CSV file is supported so far)
           example: file_lambda.txt
                    #first row of the file
                    1.
                    2.
                    3.
                    4.
                    5.
        * data: optional if filename name provided. Array of lambda

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
            if (data is not None):
                if (not type(data) is np.ndarray):
                    self.lambda_array = np.array(data)
                else:
                    self.lambda_array = data
            else:
                raise ValueError("Please provide a lambda array")

        
    def load_data(self):
        """Load the data from the filename name provided"""
        
        # only loaded implemented so far !
        self.lambda_array = Utilities.load_csv(filename = self.filename)
        