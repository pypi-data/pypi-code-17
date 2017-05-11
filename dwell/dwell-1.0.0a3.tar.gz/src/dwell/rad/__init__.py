#
def data_filename(modname, filename):
    """Given the module name, and filename, finds the path to the file from the python sys.modules
    dictionary. Used to access the header dictionary file"""
    import os, sys
    filename = os.path.join(
        os.path.dirname(sys.modules[modname].__file__),
        filename)
    return filename
    
