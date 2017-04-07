import os
curdir = os.path.abspath(os.path.dirname(__file__))
local_table = os.path.join(curdir, 'data/material_list.dat')
config_file = os.path.join(curdir, 'config.cfg')

# This makes Travis happy !
#local_table = 'python/neutronbraggedge/data/material_list.dat'
#config_file = 'python/config.cfg'
