"""
This class will retrieve the table from the URL and reformat it to be able to 
quickly retrieve the metadata for a given material
"""
#import os
import pandas as pd
import configparser
from ..config import config_file as config_config_file
from ..config import local_table as config_local_table


class RetrieveMetadataTable(object):
    """ Metadata table retriever 
    
    This class retrieves the metadata table that will allow us to get the lattice
    parameter and the crystal structure for a given material. 
    
    
    By default the program will retrieve the local version, but the web version can be retrieved
    by using the local_version=False flag. In this case, the table is retrieved from the following
    web page: `Lattice constant 
    <https://en.wikipedia.org/wiki/Lattice_constant>`.  

    >>> from braggedge.material_hanlder.retrieve_metadata_table import RetrieveMetadataTable
    >>> retrieve_local_meta = RetrieveMetadataTable()
    >>> _table = retrieve_local_meta.get_table()
    
    >>> retrieve_url_meta = RetrieveMetadataTable()
    >>> _table = retrieve_url_meta.get_table(use_local_table = False)
    
    """
    
    def __init__(self, use_local_table=True):
        self.use_local_table = use_local_table
        if not use_local_table: 
            self._retrieve_url()        
        
    def _retrieve_url(self):
        """retrieve the default url defined in the top config file"""
        self._config_file = config_config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(self._config_file)
        self.url = config_obj['DEFAULT']['material_metadata_url']
        
    def retrieve_table(self):
        """retrieve the table that contain the material/lattice parameters....
        by default, the local version is retrieved first, but the web version can
        be selected instead by using False on use_local_table flag
        
        """
        if self.use_local_table:
            self.retrieve_table_local()
        else:
            self.retrieve_table_from_url()
            
    def retrieve_table_local(self):
        """retrieve the local table"""
        self._local_table_file = config_local_table
        local_table = pd.read_csv(self._local_table_file)
        _table = local_table.set_index("Material")
        self.table = _table

    def retrieve_table_from_url(self):
        """retrieve the table using the url defined in the config.cfg file"""
        table_list = pd.read_html(self.url)
        self.raw_table = table_list[0]
        self.format_table_from_url()
        
    def format_table_from_url(self):
        """reformat the table from the url to easily extrade the metadata"""
        _table = self.raw_table
        _table.columns = _table.values[0][:]
        _table = _table[1:]
        _table = _table.set_index('Material')
        self.table = _table

    def get_table(self):
        """return the table (via url or locally) according to flag used
        
        Args:
        use_local_table (boolean): get the local table or via the url defined in the config file (default True)

        Returns:
        Pandas table of material/lattice parameters ...

        """
        self.retrieve_table()
        return self.table
