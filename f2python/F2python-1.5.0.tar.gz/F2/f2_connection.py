"""
F2 Database API
---------------

Definition of   F 2 _ C o n n e c t i o n, 

the traditional DB accessor of a database API.
Also contains the f2_caster: the mapping between
python code classes and F2 classes. 

Th. Estier

version 1.2 - june 2005
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""
import transaction
from F2 import OFF

from . import f2_object
from .f2_class  import theClass
from .f2_database import theDatabase
from .f2_helper import F2_Helper


####################  F 2 _ C o n n e c t i o n  ####################

class F2_Connection:
    "an object accessor for a F2 database storage."
    
    def __init__(self, storage_name = 'file:root.db', u='', p='', alt_c=None):
        """The storage_name may have three forms: 
           - file:<local pathname to file storage>
           - rpc:<host_address>:<port_number>
           - shared:
           In the later case, an alternate connection is given in alt_c
        """
        OS = OFF.OFFStore(storage_name, username=u, passwd=p, alt_connection=alt_c)
        self.OFFStore = OS
        self.db_root = OS.db_root
        self.connection = OS.connection
        self.db = OS.db
        OFF.cache_functions(OS)
        self.fix_registered_Python_Klasses()
        self.utility = F2_Helper(self)
            
    def __getattr__(self, name):
        """ db_connection.name  where name can be one of:
                - className
                - databaseName
        """
        if len(name) > 2 and name[0:2]== '__': # reserved name, lookup fails
            raise AttributeError(name)
        else:
            try:
                return theDatabase(name)
            except AttributeError:
                return theClass(name)
            
    def pack(self):
        "require F2 storage to squeeze/pack allocated storage ressources (files, tables, etc.)"
        self.db.pack()
    
    def commit(self):
        transaction.commit()
        self.connection.sync()
        
    def rollback(self):
        transaction.abort()
        self.connection.sync()
        
    def sync(self):
        self.connection.sync()
        
    def close(self, commit_needed=True):
        "last operation on F2_Connection before application stops."
        self.OFFStore.close(commit_needed)
        
    ########################################
    # Utilities (see comments in F2_Helper)
    ########################################
    def class_create(self, className, superClass=None, schema={}, database=None):
        return self.utility.class_create(className, superClass, schema, database)

    def add_key(self, ofClass, *attributeNames):
        """A syntactic shortcut for adding a key to a CLASS, equivalent
        to creating an object in class Key. """
        return self.utility.add_key(ofClass, *attributeNames)

    def json_repr(self, some_value, depth=1, using=None):
        """Produces a JSON representation of some_value, which may  
        be either a single F2_Object, or a F2_Object_list. Recursively represents
        included values down to specified depth. If using is specified, then
        it is a list of attributes to be used to display the values. If using=None,
        then all attributes applicable to this value (included inherited attributes) will
        be used. """
        return self.utility.json_repr(some_value, visited_objs=None, using=using, depth=depth)

    def html_repr(self, some_value, depth=1,  using=None):
        """Produces an HTML representation of some_value, which may  
        be either a single F2_Object, or a F2_Object_list. Recursively represents
        included values down to specified depth. If using is specified, then
        it is a list of attributes to be used to display the values. If using=None,
        then all attributes applicable to this value (included inherited attributes) will
        be used. """
        return self.utility.html_repr(some_value, visited_objs=None, using=using, depth=depth)
        
    # internal utility : don't call it out of the connection constructor __init__().
    def fix_registered_Python_Klasses(self):
        "tune mapping between F2 classes and Python representatives"
        new_caster = { }
        for f2_k, Python_Klass in f2_object.python_caster.items():
            if hasattr(Python_Klass, 'class_schema'):
                c_s = Python_Klass.class_schema
                if callable(c_s):
                    Python_Klass.class_schema(f2_db=self)
            try:
                new_caster[theClass(f2_k)._rank] = Python_Klass
            except:
                new_caster[f2_k] = Python_Klass
        f2_object.python_caster = new_caster
    
    