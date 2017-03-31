"""
Programatically generate nginx configurations using the objects in this module.
The objects in this submodule are based on code from https://github.com/FeroxTL/pynginxconfig-new
"""
from .blocks import EmptyBlock, Block, Location
from .options import KeyOption, KeyValueOption, KeyMultiValueOption

__all__ = [
    'EmptyBlock',
    'Block',
    'Location',
    'KeyOption',
    'KeyValueOption',
    'KeyMultiValueOption',
    'Config',
    'Section'
]

# aliases
Config = EmptyBlock
Section = Block
