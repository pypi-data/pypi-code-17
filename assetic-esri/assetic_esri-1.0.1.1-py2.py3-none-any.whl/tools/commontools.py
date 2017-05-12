# coding: utf-8
"""
    assetic_esri.tools.commontools  (commontools.py)
    Tools to assist with using arcgis integration with assetic
"""
from __future__ import absolute_import

import arcpy
import pythonaddins
import six

class CommonTools(object):
    """
    Class of tools to support app
    """

    def __init__(self, layerconfig=None):
        
        ##Test if running in desktop.  Affects messaging
        self.is_desktop = True
        try:
            chk = pythonaddins.GetSelectedCatalogWindowPath()
        except RuntimeError:
            self.is_desktop = False

    def new_message(self,message,typeid = None):
        """
        Create a message dialogue for user if desktop, else print message
        :param message: the message string for the user
        :param typeid: the type of dialog.  Integer.  optional,Default is none
        :returns: The dialog response as a unicode string, or None
        """
        res = None
        if self.is_desktop == True:
            try:
                res = pythonaddins.MessageBox(
                    message,"Assetic Integration",typeid)
            except RuntimeError:
                print("Assetic Integration: {0}".format(message))
            except Exception as ex:
                print("Unhandled Error: {0}. Message:{1}".format(
                    str(ex),message))
        else:
            print("Assetic Integration: {0}".format(message))
        return res
        
class DummyProgressDialog():
    """
    This class is used when not running arcMap in desktop mode since the
    pythonaddins ProgressDialog will have an exception.  It has to be run
    via a with statement, so this class provides an alternate with statement
    """
    def __init__(self):
        pass

    def __enter__(self):
        return True
    
    def __exit__(self,*args):
        return False
