import unittest
import os
import numpy as np
from neutronbraggedge.experiment_handler.tof import TOF
from neutronbraggedge.experiment_handler.lambda_wavelength import LambdaWavelength
from neutronbraggedge.experiment_handler.experiment import Experiment


class ExperimentTest(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../data'))

    def test_experiment_value_error_when_no_tof_provided(self):
        """Assert in experiemnt - that ValueError is raised when tof array is missing"""
        self.assertRaises(ValueError, Experiment)

    def test_experiment_value_error_when_missing_argument_for_lambda_calculation(self):
        """Assert in experiment - that ValueError is raised when detector_offset or LDS are missing for lambda calculation"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        self.assertRaises(ValueError, Experiment, _tof)
        self.assertRaises(ValueError, Experiment, _tof, None, 1)
        self.assertRaises(ValueError, Experiment, _tof, None, None, 2)
        
    def test_experiment_value_error_when_lambda_provided_and_either_lds_or_offset_missing(self):
        """Assert in experiment - that ValueError is raised when LdS and offset are missing when lambda provided"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        _lambda = [11., 12., 13., 14., 15., 16., 17.]
        self.assertRaises(ValueError, Experiment, _tof, _lambda)

    def test_experiment_value_error_when_lambda_and_tof_not_same_size(self):
        """Assert in experiment - that ValueError is raised when tof and lambda array do not have the same size"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        _lambda = [11., 12., 13., 14., 15.]
        self.assertRaises(ValueError, Experiment, _tof, _lambda, 10)
        
    def test_experiment_calculate_main_coefficient(self):
        """Assert in experiment - the calculation of main coefficient is correct"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _distance_source_detector_m = 1.609
        _detector_offset_s = 4500e-6
        _exp_obj = Experiment(tof = _tof_obj.tof_array,
                              distance_source_detector_m = _distance_source_detector_m,
                              detector_offset_micros = _detector_offset_s)
        self.assertAlmostEqual(2.45869e-7, _exp_obj._h_over_MnLds, delta = 0.0001)
    
    def test_experiment_calculate_lambda(self):
        """Assert in experiment - the calculation of lambda is correct"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _distance_source_detector_m = 1.609
        _detector_offset_micros = 4500
        _exp_obj = Experiment(tof = _tof_obj.tof_array,
                              distance_source_detector_m = _distance_source_detector_m,
                              detector_offset_micros = _detector_offset_micros)
        _lambda_expected = np.array([1.10664704e-09, 1.10916474e-09, 1.11168244e-09, 1.11420014e-09,
                                     1.11671784e-09, 1.11923554e-09, 1.12175324e-09, 1.12427094e-09,
                                     1.12678864e-09, 1.12930634e-09, 1.13182403e-09, 1.13434173e-09,
                                     1.13685943e-09, 1.13937713e-09, 1.14189483e-09, 1.14441253e-09,
                                     1.14693023e-09, 1.14944793e-09, 1.15196563e-09, 1.15448333e-09])
        _lambda_returned = _exp_obj.lambda_array
        self.assertTrue(_lambda_expected[0], _lambda_returned[0])
        self.assertTrue(_lambda_expected[5], _lambda_returned[5])
        self.assertTrue(_lambda_expected[-1], _lambda_returned[-1])
        self.assertTrue(len(_lambda_expected), len(_lambda_returned))
        
    def test_create_csv_lambda_file(self):
        """Assert in Experiment - the lambda file is correctly exported"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _distance_source_detector_m = 1.609
        _detector_offset_micros = 4500
        _exp_obj = Experiment(tof = _tof_obj.tof_array,
                              distance_source_detector_m = _distance_source_detector_m,
                              detector_offset_micros = _detector_offset_micros)
        _output_filename = os.path.join(self.data_path, 'remove_me.txt')
        _exp_obj.export_lambda(filename = _output_filename)
        self.assertTrue(os.path.isfile(_output_filename))
        os.remove(_output_filename) # cleanup temp file
        
    def test_create_csv_lambda_file_without_providing_name(self):
        """Assert in Experiment - no file is created if no filename is provided"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _distance_source_detector_m = 1.609
        _detector_offset_micros = 4500
        _output_file_name = os.path.join(self.data_path, 'no_file.txt')
        _exp_obj = Experiment(tof = _tof_obj.tof_array,
                              distance_source_detector_m = _distance_source_detector_m,
                              detector_offset_micros = _detector_offset_micros)
        self.assertRaises(ValueError, _exp_obj.export_lambda)

    def test_calculate_distance_source_detector(self):
        """Assert in Experiment - the distance source detector is corectly calculated"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _detector_offset_micros = 4500
        _lambda_file = os.path.join(self.data_path, 'lambda.txt')
        _lambda_obj = LambdaWavelength(filename = _lambda_file)
        _tof_array = _tof_obj.tof_array[0:20]
        _lambda_array = _lambda_obj.lambda_array[0:20]

        _exp_handler = Experiment(tof = _tof_array,
                                  lambda_array = _lambda_array,
                                  detector_offset_micros = _detector_offset_micros)
        _distance_expected = 1.609 #m
        _distance_returned = _exp_handler.distance_source_detector
        self.assertAlmostEqual(_distance_expected, _distance_returned, delta = 1e-6)
        
    def test_calculate_detector_offset(self):
        """Assert in Experiment - the detector offset is correctly calculated"""
        _tof_file = os.path.join(self.data_path, 'tof.txt')
        _tof_obj = TOF(filename = _tof_file)
        _distance_source_detector_m = 1.609
        _lambda_file = os.path.join(self.data_path, 'lambda.txt')
        _lambda_obj = LambdaWavelength(filename = _lambda_file)
        _tof_array = _tof_obj.tof_array[0:20]
        _lambda_array = _lambda_obj.lambda_array[0:20]

        _exp_handler = Experiment(tof = _tof_array,
                                  lambda_array = _lambda_array,
                                  distance_source_detector_m = _distance_source_detector_m)
        _offset_expected_micros = 4500 #micros
        _offset_calculated = _exp_handler.detector_offset_micros
        self.assertAlmostEqual(_offset_expected_micros, _offset_calculated, 
                               delta = 1e-6)

if __name__ == '__main__':
    unittest.main()
