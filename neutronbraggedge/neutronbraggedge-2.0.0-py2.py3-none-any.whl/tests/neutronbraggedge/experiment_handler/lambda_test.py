import unittest
import os
import numpy as np
from neutronbraggedge.experiment_handler.lambda_wavelength import LambdaWavelength


class TofTest(unittest.TestCase):

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../data'))

    def test_loading_manual_lambda_array(self):
        """Assert in LambdaWavelength - manual loading of array"""
        _lambda_array = [1., 2., 3., 4., 5., 6., 7., 8., 9.]
        _lambda_handler = LambdaWavelength(data = _lambda_array)
        self.assertTrue(all(_lambda_array == _lambda_handler.lambda_array))

    def test_loading_normal_array_data(self):
        """Assert in LambdaWavelength - loading of np.array array"""
        _lambda_array = np.array([1, 2., 3., 4.])
        _lambda_handler = LambdaWavelength(data = _lambda_array)
        self.assertTrue(all(_lambda_array == _lambda_handler.lambda_array))

    def test_not_lambda_array_provided(self):
        """Assert in LambdaWavelength - no lambda array provided"""
        self.assertRaises(ValueError, LambdaWavelength)

    def test_loading_auto_lambda_array(self):
        """Assert in LambdaWavelength - auto loading of array"""
        _lambda_filename = os.path.join(self.data_path, 'lambda.txt')
        _lambda_handler = LambdaWavelength(filename = _lambda_filename)
        _lambda_expected = np.array([1.10664703784e-09, 1.10916473754e-09, 1.11168243725e-09,
                                     1.11420013696e-09, 1.11671783666e-09, 1.11923553637e-09,
                                     1.12175323607e-09, 1.12427093578e-09, 1.12678863549e-09,
                                     1.12930633519e-09, 1.1318240349e-09, 1.1343417346e-09,
                                     1.13685943431e-09, 1.13937713401e-09, 1.14189483372e-09,
                                     1.14441253343e-09, 1.14693023313e-09, 1.14944793284e-09,
                                     1.15196563254e-09, 1.15448333225e-09]) 
        self.assertTrue(all(_lambda_expected[0:5] == _lambda_handler.lambda_array[0:5]))

    def test_load_bad_file_name(self):
        """Assert in LambdaWavelength - file name is provided but does not exist"""
        _lambda_filename = os.path.join(self.data_path, 'i_do_not_exist.txt')
        self.assertRaises(IOError, LambdaWavelength, _lambda_filename)

if __name__ == '__main__':
    unittest.main()
