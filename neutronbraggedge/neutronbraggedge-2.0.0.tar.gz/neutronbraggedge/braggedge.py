from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator
from .utilities import Utilities
import os


class BraggEdge(object):
    """This is from where the user will retrieve all metadata and calculation
        
    Variables:
        
      From **python**, first you need to import the package

    >>> from braggedge.braggedge import BraggEdge
    
    For a particular element you can retrieve:
     - lattice parameter
     - h, k and l values
     - Crystal structure
     - bragg edges values
     
    For this example, we are retrieving the data for *Fe* and we are only
    interested by the first *4* crystal orientation.
    
    >>> _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
    >>> print("Crystal Structure is: %s" %_handler.metadata['cyrstal_structure]))
    'BCC'
    >>> print("Lattice is %.2f" %_handler.metadata['lattice'])
    2.87
    >>> print("hkl are: " , _handler.hkl)
    hkl are: [][1,1,0],[2,0,0],[2,1,1],[2,2,0]]
    >>> print("bragg edges are: ", _handler.bragg_edges)
    bragg edges are: [2.0268, 1.4332, 1.1702, 1.0134]
    
    
    It is also possible to display all metadata at once
    
    >>> print(_handler)
    ===================================
    Material: Fe
    Lattice: 2.8664A
    Crystal Structure: BCC
    Using local metadata Table: True
    ===================================
     h | k | l |   d(A)  |    BraggEdge
    ===================================
     1 | 1 | 0 |  2.0269 |    4.0537
     2 | 0 | 0 |  1.4332 |    2.8664
     2 | 1 | 1 |  1.1702 |    2.3404
     2 | 2 | 0 |  1.0134 |    2.0269
    ===================================
    
    Then you can export the resulting metadata into a CSV file
    
    >>> _handler.export(filename = 'my_file_name.txt')
    
    """
    
    hkl = None
    metadata = None
    bragg_edges = None
    d_spacing = None
    
    def __init__(self, material=None, 
                 new_material = None,
                 number_of_bragg_edges=10, 
                 use_local_metadata_table=True):
        """
        Constructor
        
        Arguments:
           - material: name of the material such as 'Ni', 'Fe' ...
           - new_material: dictionary of new materials defined as
              [{'name': 'Ta',
               'lattice': 0.333,
               'crystal_structure': 'FCC'},
               {'name': 'Ur',
               'lattice': 0.5555,
               'crystal_structure': 'BCC'}]
           - number_of_bragg_edge:  Default 10. Number of row to display and calculate data for.
           - use_local_metadata_table: default True. Use local defined table to retrieve lattice parameters,
                                     crystal structure. If False, will go to wiki web page.
        
        """

        if material is None:
            if new_material is None:
                raise ValueError("No material or new_material defined!")
            else:
                #parse dictionary
                list_material = []
                try:
                    
                    for _element in new_material:
                        _name = _element['name']
                        list_material.append(_name)
                        _lattice_constant = _element['lattice']
                        _crystal_structure =  _element['crystal_structure']
                except:
                    raise ValueError("Check the format of the new element array!")
                    
                material = list_material

        if not (type(material) is list):
            material = [material]

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table
        
        self._retrieve_metadata(new_material = new_material)
        self._calculate_hkl()
        self._calculate_braggedges()
        
    def get_experimental_lattice_parameter(self, experimental_bragg_edge_values = None,
                                    experimental_bragg_edge_error = None):
        """calculates the experimental lattice parameter values given an array of 
        bragg edge values"""
        
        if experimental_bragg_edge_error is None:
            raise ValueError("Please provide an array of bragg edge values")
        
        if experimental_bragg_edge_error is not None:
            if len(experimental_bragg_edge_error) != len(experimental_bragg_edge_values):
                raise ValueError("Make sure exp. bragg edge value and error have the same size!")
        
        _calculator = self._calculator
        _calculator.calculate_lattice_array(experimental_bragg_edge_values,
                                            experimental_bragg_edge_error)
        exp_lattice_parameter = _calculator.lattice_experimentatl
        return exp_lattice_parameter
        
    def _retrieve_metadata(self, new_material=None):
        """This method retrieves the lattice and crystal structure of the material"""
        _lattice = {}
        _crystal_structure = {}

        if new_material is None: #retrieve infos from ascii table
            for _material in self.material:
                _handler = RetrieveMaterialMetadata(material = _material,
                                                    use_local_table = self.use_local_metadata_table)
                _lattice[_material] = _handler.lattice
                _crystal_structure[_material] = _handler.crystal_structure
                
        else: #local infos
            for _element in new_material:
                _material = _element['name']
                _local_lattice = _element['lattice']
                _local_crystal_structure =  _element['crystal_structure']

                _lattice[_material] = _local_lattice
                _crystal_structure[_material] = _local_crystal_structure

        self.lattice = _lattice
        self.crystal_structure = _crystal_structure
    
        self.metadata = {'lattice': self.lattice, 
                'crystal_structure': self.crystal_structure}

    def _calculate_hkl(self):
        """This method calculate the set of hkl up to the number_of_bragg_edges specified"""
        calculator = {}
        _hkl = {}
        
        for _material in self.material:
            _structure_name = self.metadata['crystal_structure'][_material]
            _lattice = self.metadata['lattice'][_material]
            
            _calculator = BraggEdgeCalculator(structure_name = _structure_name,
                                              lattice = _lattice,
                                              number_of_set = self.number_of_bragg_edges)
            
            _calculator.calculate_hkl()
            calculator[_material] = _calculator
            _hkl[_material] = _calculator.hkl

        self._calculator = calculator
        self.hkl = _hkl

    def _calculate_braggedges(self):
        """This method calculates the braggedges values (and the d_spacing in the same time)"""
        _d_spacing = {}
        _bragg_edges = {}

        
        for _material in self.material:
            _calculator = self._calculator[_material]
            
            _calculator.calculate_bragg_edges()
            _d_spacing[_material] = _calculator.d_spacing
            _bragg_edges[_material] = _calculator.bragg_edges

        self.d_spacing = _d_spacing
        self.bragg_edges = _bragg_edges
        
    def __repr__(self):
        """Display the metadata/hkl/d_spacing/bragg edge values"""
        nbr_ticks = 45
        
        for _material in self.material:

            print('=' * nbr_ticks)
            print("Material: %s" %_material)
            print(u"Lattice : %.4f\u212B" %self.metadata['lattice'][_material])
            print("Crystal Structure: %s" %self.metadata['crystal_structure'][_material])
            print("Using local metadata Table: %s" %self.use_local_metadata_table)
            print('=' * nbr_ticks)
            print(u" h | k | l |\t d (\u212B)  |\t BraggEdge")
            print('-' * nbr_ticks)

            _hkl = self.hkl[_material]
            _bragg_edges = self.bragg_edges[_material]
            _d_spacing = self.d_spacing[_material]
        
            for index in range(len(_d_spacing)):
                print(" %d | %d | %d |\t %.5f |\t %.5f" %(_hkl[index][0],
                                                          _hkl[index][1],
                                                          _hkl[index][2], 
                                                          _d_spacing[index],
                                                          _bragg_edges[index]))
        
            print('=' * nbr_ticks)


        return ""
        
    def export(self, filename=None, file_type='csv'):
        """Export the metadata into various file format
        
        Arguments:
        
           filename: output file name to create
           file_type: format of the file to create
              only 'csv' (simple comma separated format) is supported for now
            
        Exception:
           IOError: if no file name is provided
        
        """
        if filename is None:
            raise IOError

        for _material in self.material:
            
            _filename = self._format_filename(filename, _material)
            _metadata = self._format_metadata(_material)
            _data = self._format_data(_material)
            
            if file_type is 'csv':
                Utilities.save_csv(filename = _filename,
                                   data = _data,
                                   metadata = _metadata)
        
            else:
                raise NotImplementedError
        
        
    def _format_filename(self, filename, material):
        _filename, _extension = os.path.splitext(filename)
        new_filename = os.path.join(_filename + '_' + material + _extension)
        return new_filename
        
    def _format_metadata(self, _material):
        """Format the various metadata to put at the top of output file created"""
        _metadata = []
        _metadata.append("Material: %s" %_material)
        _metadata.append("Lattice : %.4fAngstroms" %self.metadata['lattice'][_material])
        _metadata.append("Crystal Structure: %s" %self.metadata['crystal_structure'][_material])
        _metadata.append("Using local metadata Table: %s" %self.use_local_metadata_table)
        _metadata.append("")
        _metadata.append("h, k, l, d(Angstroms), BraggEdge")
        return _metadata
    
    def _format_data(self, _material):
        """Format the data for the output file created"""
        _data = []
        _hkl = self.hkl[_material]
        _bragg_edges = self.bragg_edges[_material]
        _d_spacing = self.d_spacing[_material]
        for index in range(len(_d_spacing)):
            _data.append([_hkl[index][0],
                         _hkl[index][1],
                         _hkl[index][2],
                         _d_spacing[index],
                         _bragg_edges[index]])
        return _data

