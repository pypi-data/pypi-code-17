"""
This class will automatically retrieve the lattice parameter and the crystal structure of a given
element
"""
from .retrieve_metadata_table import RetrieveMetadataTable


class RetrieveMaterialMetadata(object):
    """ Retrieve the metadata for a given material 
    
    This class retrieves the lattice parameter and the crystal structure 
    of a given material.
    
    >>> from braggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
    >>> retrieve_metadata = RetrieveMaterialMetadata("Si")
    >>> print ("Structure is: %s" %retrieve_metadata.crystal_structure)
    Structure is: FCC
    >>> print ("Lattice parameter is %.2f Angstroms" %retrieve_metadata.lattice)
    Lattice parameter is 5.43 Angstroms
    
    """
    
    lattice = None
    crystal_structure = None
    
    def __init__(self, material=None, use_local_table=True):
        """Constructor that will automatically retrieve the metadata
        
        Args:
        material: mandatory string (ex: "Si")
        use_local_table: optional boolean. By default, a local table is used, but
           user can turn off the flag to retrieve data from web site 
           (`<https://en.wikipedia.org/wiki/Lattice_constant>`)
        
        Exception:
        NameError: if no material is given
        """
        if material is None:
            raise NameError("Please provide a material")
        

        self._material = material
        self.use_local_table = use_local_table

        self._retrieve_table()
        if not (material.lower() == 'all'):
            self._retrieve_metadata()
        
    def _retrieve_table(self):
        """retrieve the table """
        metadata_table = RetrieveMetadataTable()
        self.table = metadata_table.get_table()

    def full_list_material(self):
        _list_material = self.table.index.values
        return _list_material
        
    def _retrieve_metadata(self):
        """retrieve the metadata ('lattice constant','crystal structure')"""
        try:
            _metadata = self.table.loc[self._material]
        except KeyError:
            raise KeyError("Material unknown")
        self._retrieve_lattice(_metadata)
        self._retrieve_crystal_structure(_metadata)
        
    def _retrieve_lattice(self, _metadata):
        self.lattice = float(_metadata[0])
        
    def _retrieve_crystal_structure(self, _metadata):
        _full_crystal_str = _metadata[1]

        if 'FCC' in _full_crystal_str:
            _crystal_str = 'FCC'
        elif 'BCC' in _full_crystal_str:
            _crystal_str = 'BCC'
        else:
            raise NameError("Crystal Structure not supported yet!")
        self.crystal_structure = _crystal_str
    
