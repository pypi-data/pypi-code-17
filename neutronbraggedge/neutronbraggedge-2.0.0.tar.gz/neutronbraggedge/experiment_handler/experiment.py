import numpy as np
from .tof import TOF
from ..constants import mn, h
from ..utilities import Utilities

class Experiment(object):
    """Class that allows:
       - convert the TOF scale into Lambda
       - distance source - detector
       - detector time offset
       
       Arguments:
       * tof: tof array in s
       * lambda_array: mandatory only if detector_offset or distance_source_detector are unknown
       * distance_source_detector: mandatory only if lambda is the unknown parameter (m)
       * detector_offset: mandatory only if lambda is the unknown parameter (micros)
       """
    
    def __init__(self, tof=None, lambda_array=None, 
                 distance_source_detector_m=None, 
                 detector_offset_micros=None):
        if tof is None:
            raise ValueError("Missing TOF array")
        self.tof_array = tof
        self.distance_source_detector = distance_source_detector_m
        self.detector_offset_micros = detector_offset_micros
        self.lambda_array = lambda_array

        # if lambda_array is unknown, both distance_source_detector and detector_offset must be provided
        if lambda_array is None:
            if (distance_source_detector_m is None) or (detector_offset_micros is None):
                raise ValueError("Mssing arguments to calculate lambda_array")

        # if lambda_array is provided, either distance_source_detector_m or detector_offset_micros can be missing,
        # but not both
        if lambda_array is not None:
            if (distance_source_detector_m is None) and (detector_offset_micros is None):
                raise ValueError("Missing either distance_source detector or detector_offset")

            if len(lambda_array) != len(tof):
                raise ValueError("TOF and Lambda do not have the same size !")

            if distance_source_detector_m is None:
                self.calculate_distance_source_detector()
            else:
                self.calculate_detector_offset()

        else:
            self.calculate_lambda()
        
    def calculate_tof_with_detector_offset(self):
        """return the tof with detector_offset applied to it"""
        detector_offset_micros = self.detector_offset_micros
        detector_offset_s = Utilities.convert_time_units(detector_offset_micros,
                                                         from_units = 'micros',
                                                         to_units = 's')
        # apply detector offset to tof array
        _tof = self.tof_array 
        _tof_with_offset = Utilities.array_add_coeff(data = _tof,
                                                     coeff = detector_offset_s)
        return _tof_with_offset        


    def calculate_distance_source_detector(self):
        """return the distance source detector
        
        If lambda_array and tof_array are provided, the distance is calculated
        Otherwise, the distance_source_detector must be provided
        """
        _tof_with_offset = self.calculate_tof_with_detector_offset() 
        
        # calculate the constant factor
        _coeff = h / mn

        # multiply constant facor by tof array
        _numerator = Utilities.array_multiply_coeff(data = _tof_with_offset, 
                                                coeff = _coeff)

        _denominator = self.lambda_array
        
        # divide numerator by denominator
        _ratio = Utilities.array_divide_array(numerator = _numerator,
                                              denominator = _denominator)

        self.distance_source_detector = np.mean(_ratio)

    def calculate_detector_offset(self):
        """return the detector time offset value
        
        If lambda_array and tof_array are provided, the offset is calculated
        Otherwise, the detector_offset argument must be provided
        """

        # calculate the constant factor
        lSD = self.distance_source_detector
        _coeff = h / (mn * lSD)
        _MnLds_over_h = 1./_coeff
        
        # lambda / coeff
        _lambda_array = self.lambda_array
        _lambda_over_coeff = Utilities.array_multiply_coeff(data = _lambda_array,
                                                            coeff = _MnLds_over_h)

        # (lambda/coeff) - tof
        _tof = self.tof_array
        
        _detector_offset_array = Utilities.array_minus_array(array1 = _lambda_over_coeff,
                                              array2 = _tof)
        _detector_offset_s = np.mean(_detector_offset_array)
        self.detector_offset_micros = Utilities.convert_time_units(data = _detector_offset_s,
                                                                   from_units = 's',
                                                                   to_units = 'micros')
        
    
    def calculate_lambda(self):
        """return the lambda array when tof_array, distance_source_detector and 
        detector_offset are provided
        """
        _tof_with_offset = self.calculate_tof_with_detector_offset() 

        # calculate the constant factor
        lSD = self.distance_source_detector
        _coeff = h / (mn * lSD)
        self._h_over_MnLds = _coeff

        # multiply constant factor by tof array
        _lambda = Utilities.array_multiply_coeff(data = _tof_with_offset, 
                                                coeff = _coeff)
            
        self.lambda_array = _lambda
        
    def export_lambda(self, filename=None):
        """export the lambda array into a CSV data file
        
        Parameters:
        * filename: name of output file to create
        """
        if filename is None:
            raise ValueError("Please provide a file name!")
        
        _metadata = []
        _metadata.append("Lambda (Angstroms)")
        _metadata.append("")
        _metadata.append("Distance source-detector (m): %.4f" %self.distance_source_detector)
        _metadata.append("Detector offset (micros): %.4f" %self.detector_offset_micros)
        _metadata.append("")
        _metadata.append("Lambda (Angstroms)")
        
        Utilities.save_csv(filename = filename, 
                           data = self.lambda_array,
                           metadata = _metadata)
        
