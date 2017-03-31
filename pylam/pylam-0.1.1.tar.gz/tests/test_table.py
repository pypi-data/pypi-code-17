#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pylam.base import (Table, zeroTable)
import numpy as np

data_in = np.empty( (10,4) )
properties = ['A', 'B', 'C', 'D']


#tbl = Table(data_in=data_in, props=properties)
tbl = zeroTable(4,14, props=properties)



import tableprint as tp
t = {'rtime': 20.8144, 'steps': 10000, 'mempp': 4.18164, 'thermo': 100, 'procs': 16, 'atoms': 1372}

from pylam.base import dict2table
tp.banner('runprops')
dict2table(t,headers=None)




