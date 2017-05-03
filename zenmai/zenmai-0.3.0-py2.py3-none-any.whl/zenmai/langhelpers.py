import magicalimport


def import_module(path, here=None):
    if path.endswith(".py"):
        return magicalimport.import_from_physical_path(path, here=here)
    else:
        return magicalimport.import_module(path)


import_symbol = magicalimport.import_symbol
