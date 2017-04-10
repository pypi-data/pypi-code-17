"""
F2 Database Interface
---------------------

Provides primitive access to an F2 Database content. This layer is
built immediately on top of module OFF. Defines the most generic
class for F2 objects handles: F2_Object(), and some specific
subclasses: F2_Class(), F2_Attribute(), etc...

Th. Estier

version 1.5.0 - january 2017
   --
   written after the original Ada version from 1989-1990, Th. Estier, CUI Geneva.
"""

__all__ = ["F2_Object", "theObject", "F2_Object_list", "F2_NULL", 
           "F2_Class", "theClass", 
           "F2_Attribute", "theAttribute",
           "F2_Database", "theDatabase",
           "F2_Key",
           "F2Error", "F2ValueError", "F2AttributeError", "F2TypeError", "ClassDesignationError",
           "connect", "_RegisterPythonClass"]


from .f2_object import F2_Object, theObject, F2_Object_list, F2_NULL
from .f2_class import F2_Class, theClass
from .f2_attribute import F2_Attribute, theAttribute
from .f2_database import F2_Database, theDatabase
from .f2_key import F2_Key
from .f2_connection import F2_Connection

from .f2_object import F2Error, F2ValueError, F2AttributeError, F2TypeError, ClassDesignationError


def connect(storage_name = 'file:root.db', username='', passwd='', alt_connect=None):
    """Opens an F2 database connection and returns an accessor.
       The storage_name may have three forms:
           - file:<local pathname to file storage>
           - rpc:<host_address>:<port_number>
           - shared:
       In the 3rd case, a connection is already open on some storage, and is
       passed in parameter alt_connect.
     """
    return F2_Connection(storage_name, u=username, p=passwd, alt_c=alt_connect)

from .f2_object import _RegisterPythonClass



