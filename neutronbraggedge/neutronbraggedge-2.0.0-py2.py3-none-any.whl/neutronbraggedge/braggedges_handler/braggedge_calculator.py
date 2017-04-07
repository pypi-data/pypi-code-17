import sys
import numpy as np
import configparser
from .structure_handler import StructureHandler
from ..config import config_file as config_config_file


class BraggEdgeCalculator(object):
    """
    This class calculates the h, k, and l values allowed for the given structure.
    The number of h,k,l set is by default set to 10 but can be changed
    
    Args:
    structure_name: default 'FCC'. Must be either ['FCC', 'BCC']
    
    """
    
    def __init__(self, structure_name="FCC", lattice=None, number_of_set=10):
        self.structure = structure_name #only used to test validity of input
        self._structure = structure_name
        self._number_of_set = number_of_set
        self.lattice = lattice

    @property
    def structure(self):
        return self._structure
    
    @structure.setter
    def structure(self, structure_name):
        
        _config_file = config_config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(_config_file)
        self._list_structure = config_obj['DEFAULT']['list_structure']
        
        if not (structure_name in self._list_structure):
            raise ValueError("Structure name should be in the list " , self._list_structure)
        self._structure = structure_name
        
    def calculate_hkl(self):
        _structure_handler = StructureHandler(structure = self._structure,
            number_of_set = self._number_of_set)      
        self.hkl = _structure_handler.hkl
        
    def calculate_bragg_edges(self):
        """This calculate the d_spacing and bragg edges of the various h, k and l"""
        if self.lattice is None:
            raise ValueError
        
        _bragg_edges_array = []
        _d_spacing = []
        for _hkl in self.hkl:
            _result = self._calculate_individual_bragg_edge(lattice = self.lattice,
                                                            h = _hkl[0],
                                                            k = _hkl[1],
                                                            l = _hkl[2])
            _d_spacing.append(_result)
            _bragg_edges_array.append(2. * _result)
        self.bragg_edges = _bragg_edges_array
        self.d_spacing = _d_spacing
            
    def _calculate_individual_bragg_edge(self, lattice=None,
                                         h=1, k=1, l=1):
        _den = np.sqrt(h**2 + k**2 + l**2)
        return float(lattice)/_den
        
    #def _calculate_individual_lattice(self, h=1, k=1, l=1, bragg_edge_value=0, bragg_edge_error=0):
        #_num = np.sqrt(h**2 + k**2 + l**2)
        #_value = float(bragg_edge_value/2.)*_num
        #_error = float(bragg_edge_error/2.)*_num
        #return [_value, _error]
        
    #def calculate_lattice_array(self, exp_bragg_edge_value, exp_bragg_edge_error=None):
        #"""calculate the lattice given the hkl and bragg edge value"""
        #_lattice_array = []
        #_lattice_error_array = []
        #for _index, _hkl in enumerate(exp_bragg_edge_value):
            #_hkl = self.hkl[_index]
            #_bragg = exp_bragg_edge_value[_index]
            
            #if exp_bragg_edge_error is not None:
                #_error = exp_bragg_edge_error[_index]
            #else:
                #_error = 0
            #[_result, _result_error] = self._calculate_individual_lattice(h = _hkl[0],
                                                                   #k = _hkl[1],
                                                                   #l = _hkl[2],
                                                                   #bragg_edge_value = _bragg,
                                                                   #bragg_edge_error = _error)
            #_lattice_array.append(_result)
            #_lattice_error_array.append(_result_error)
        
        #self.lattice_experimental = _lattice_array
        #self.lattice_error_experimental = _lattice_error_array
            
        #self.average_lattice_experimental = self._calculate_average_lattice_experimental()
        
    #def _calculate_average_lattice_experimental(self):
        #_lattice_exp = self.lattice_experimental
        #_lattice_error_exp = self.lattice_error_experimental
        
        #_mean_value = np.mean(_lattice_exp)
        #_sum_error = 0
        #for _error in _lattice_error_exp:
            #_sum_error += _error * _error
        
        #_mean_error = np.sqrt(_sum_error)
        
        #self.mean_lattice_experimental = [_mean_value, _mean_error]
        
        
        
        