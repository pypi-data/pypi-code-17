import os
import sys
import importlib

# Loop over every directory beneath us that has a __init__.py inside of it
root_dir = os.path.dirname(__file__)
for module_name in os.listdir(root_dir):
    if not os.path.isdir(os.path.join(root_dir, module_name)) or not os.path.isfile(os.path.join(root_dir, module_name, '__init__.py')):
        continue

    # Import this module
    importlib.import_module(__name__ + '.' + module_name)

# Cleanup thse dangling bindings
del importlib
del module_name
del root_dir
del os
del sys
