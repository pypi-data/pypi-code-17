"""Columnar records is a datastructure that contains a named list of array
It will eventually support all the same concepts as a record array or
data frame, but should hopefully be easier to reason about and more efficient

At it's root, it only needs two pieces of data:
a list of arrays and a list of names

In fact, you could actually think of the whole thing as an ordered dict of arrays.

Major methods implemented:

sort and argsort - return new CR's and use np.lexsort internally
get_index_groups - a port of np_utils.get_index_groups for CR's and can be used to implement grouping operations
apply and applyargs - apply any function to the arrays of the CR and return a new CR
indexing and slicing [] -  all array and dataframe-like operations are supported,
                           returing arrays or CR's where appropriate
equality, comparisons - all standard comparisons work (=,<,>), including array_equals
conversion to and from major formats is supported: lists of arrays, record arrays, and record tuples
"""

from __future__ import print_function, division, absolute_import
from builtins import range, zip, str, map
from past.builtins import basestring

from functools import reduce

import numpy as np

from . import utils
from .utils import _group_transform

REPR_STR = '''ColumnarRecords([
  {}
 ],
 names={},
 dtypes={})'''

def _reducing_and(x):
    return reduce(np.logical_and, x)

def _reducing_or(x):
    return reduce(np.logical_or, x)

def equal(a, b):
    return a._binary_op(b, np.ndarray.__eq__, _reducing_and)

def not_equal(a, b):
    return a._binary_op(b, np.ndarray.__ne__, _reducing_or)

def _comp(a, b, op):
    first = True
    for i, j in zip(a.arrays, b.arrays):
        if first:
            first = False
            out = op(i, j)
            e = np.equal(i, j)
        else:
            ii, jj = i[e], j[e]
            out[e] = op(ii, jj)
            ee = np.equal(ii, jj)
            if not np.sum(ee):
                break
            e[e] = ee
    
    return out

def lt(a, b):
    return _comp(a, b, np.ndarray.__lt__)

def gt(a, b):
    return _comp(a, b, np.ndarray.__gt__)

def le(a, b):
    return _comp(a, b, np.ndarray.__le__)

def ge(a, b):
    return _comp(a, b, np.ndarray.__ge__)

def join(*colrec_list):
    '''Join two or more ColumnarObjects together'''
    return ColumnarRecords([arr for c in colrec_list
                                for arr in c.arrays],
                           [name for c in colrec_list
                                 for name in c.names])

def _has_records(x):
    return isinstance(x, np.ndarray) and x.dtype.names is not None

class ColumnarRecords(object):
    def __init__(self, arrays, names=None, dtypes=None):
        # Work-around to allow construction based on another CR:
        if isinstance(arrays, ColumnarRecords):
            return ColumnarRecords(arrays.arrays, names=arrays.names)
        
        if names is None:
            names = ['f{}'.format(i) for i in range(len(arrays))]
        
        if dtypes is None:
            arrays = [np.asanyarray(arr) for arr in arrays]
            dtypes = [arr.dtype for arr in arrays]
        else:
            arrays = [np.asarray(arr, dtype=dtype)
                      for arr, dtype in zip(arrays, dtypes)]
        
        for arr in arrays:
            assert arr.dtype.names is None, 'Arrays must not be records!'
        
        self.ncols = utils.assertSameAndCondense([len(i) for i in [arrays, dtypes, names]])
        self.shape = utils.assertSameAndCondense([arr.shape for arr in arrays])
        self.size = utils.assertSameAndCondense([arr.size for arr in arrays])
        self.length = 0 if not len(self.shape) else self.shape[0]
        
        self.arrays = arrays
        self.names = names
        self.dtypes = dtypes
        self._name_inds = {n: i for i, n in enumerate(self.names)}
    
    def index(self, key):
        if isinstance(key, basestring):
            return self.arrays[self._name_inds[key]]
        elif hasattr(key, '__len__') and len(key) and isinstance(key[0], basestring):
            return ColumnarRecords([self.arrays[self._name_inds[k]] for k in key],
                                    names=[self.names[self._name_inds[k]] for k in key])
        else:
            return ColumnarRecords([arr[key] for arr in self.arrays], names=self.names)
    
    def elements_equal(self, x):
        """Matching arrays by position only, return a list of
        self.arrays[i] == x.arrays[i]
        """
        return [i == j for i, j in zip(self.arrays, x.arrays)]
    
    def _names_match(self, x):
        x = as_cr(x)
        
        if self.ncols != x.ncols:
            return False
        
        if any([i!=j for i, j in zip(self.names, x.names)]):
            return False
        
        return True
    
    def __len__(self):
        return self.length
    
    def __getitem__(self, key):
        return self.index(key)
    
    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            self.arrays[self._name_inds[key]] = value
        elif hasattr(key, '__len__') and len(key) and isinstance(key[0], basestring):
            if _has_records(value):
                value = ColumnarRecords(value)
            
            if isinstance(value, ColumnarRecords):
                for k in key:
                    self.arrays[self._name_inds[k]] = value.arrays[value._name_inds[k]]
            else: # assume we have a list of arrays or give up:
                for k, v in zip(key, value):
                    self.arrays[self._name_inds[k]] = v
        else:
            if _has_records(value):
                value = ColumnarRecords(value)
            
            if isinstance(value, ColumnarRecords):
                assert self._names_match(value)
                for arr, v in zip(self.arrays, value.arrays):
                    arr[key] = v
            else: # assume we have a list of arrays or give up:
                for arr, v in zip(self.arrays, value):
                    arr[key] = v
    
    def __repr__(self):
        arr_strs = [repr(arr).replace('\n', '\n  ') for arr in self.arrays]
        return REPR_STR.format(',\n  '.join(arr_strs), self.names, self.dtypes)
    
    def _binary_op(self, x, op, reducer):
        x = as_cr(x)
        
        if not self._names_match(x):
            raise ValueError('Cannot combine CRs with mismatched names!')
        
        return reducer([op(i, j) for i, j in zip(self.arrays, x.arrays)])
    
    def array_equal(self, x):
        x = as_cr(x)
        
        if self.length != x.length:
            return False
        
        if not self._names_match(x):
            return False
            
        return self._binary_op(x, np.array_equal, all)
    
    def __eq__(self, x):
        return equal(self, x)
    
    def __ne__(self, x):
        return not_equal(self, x)
    
    def __gt__(self, x):
        return gt(self, x)
    
    def __ge__(self, x):
        return ge(self, x)
    
    def __lt__(self, x):
        return lt(self, x)
    
    def __le__(self, x):
        return le(self, x)
    
    def __iter__(self):
        return (tuple([arr[i] for arr in self.arrays])
                for i in range(self.size))
    
    def argsort(self, order=None, axis=-1):
        """Get the indices that will sort the arrays, treating the first
        array as the most significant for sorting
        If order is specified as a name or list of names,
        it will determine the order; otherwise internal order is used
        """
        order = (self.names if order is None else
                 [order] if isinstance(order, str) else
                 order)
        keys = [self.arrays[self._name_inds[i]] for i in order]
        return np.lexsort(keys[::-1], axis=axis)
    
    def sort(self, order=None, axis=-1):
        inds = self.argsort(order=order, axis=axis)
        return self.index(inds)
    
    def apply(self, f):
        """Return a new ColumnarRecords object, applying f to each array
        """
        return ColumnarRecords(map(f, self.arrays), names=self.names)
    
    def applyargs(self, f, *args, **kwds):
        """Return a new ColumnarRecords object, applying f to each array
        """
        return ColumnarRecords([f(arr, *args, **kwds) for arr in self.arrays],
                                names=self.names)
    
    def ravel(self):
        return self.apply(np.ravel)
    
    def __getslice__(self, i, j):
        return self.applyargs(np.ndarray.__getslice__, i, j)
    
    def __setslice__(self, i, j, y):
        y = as_cr(y)
        
        if self.names != y.names:
            raise Exception('Cannot set slice: names do not match!')
        
        for arr, y_arr in zip(self.arrays, y.arrays):
            arr.__setslice__(i, j, y_arr)
    
    def group_count(self, use_argsort=False):
        '''Get the count of all the groups in the array
           This is much faster than what could be acheived using the tools below,
           i.e. map(len, get_index_groups(arr)[0])'''
        rav = self[names].ravel()
        sort_rav = rav.sort()
        isdiff, keys, split_points = utils.index_helper(rav, sort_rav)
        counts = np.diff(np.concatenate((split_points, [rav.size])))
        return keys, counts
    
    def get_index_groups(self, names=None):
        if names is None:
            names = self.names
        
        if isinstance(names, basestring):
            names = [names]
        
        rav = self[names].ravel()
        sort_ind = rav.argsort()
        sort_rav = rav[sort_ind]
        b = sort_rav[1:] != sort_rav[:-1]
        isdiff, keys, split_points = utils.index_helper(rav, sort_rav)
        sorted_key_inds = np.cumsum(isdiff) - 1
        inv = np.empty(rav.shape, dtype=np.intp)
        inv[sort_ind] = sorted_key_inds
        index_groups = utils.split_at_boundaries(np.argsort(inv), split_points)
        return keys, index_groups
    
    def groupby(self, keynames, *fun_fields_name):
        '''Clone of np_utils.rec_groupby for a CR
           
           Docs for np_utils.rec_groupby:
           A special version of np_groupby for record arrays, somewhat similar
           to the function found in matplotlib.mlab.rec_groupby.
           
           This is basically a wrapper around np_groupy that automatically
           generates lambda's like the ones in the np_groupby doc string.
           That same call would look like this using rec_grouby:
           
           rec_groupby(a, ['m', 'n'], (np.mean, 'o', 'mean_o'),
                                      (np.std, 'o', 'std_o'),
                                      (np.min, 'p', 'min_p'))
           and the second function could be written as:
               def compute_some_thing(x):
                   o, p = x['o'], x['p']
                   return np.mean(o) / np.std(o) * np.min(p)
               rec_groupby(a, ['m', 'n'],
                           (compute_some_thing, ['o', 'p'], 'its_complicated'))
           
           In general, this function is faster than matplotlib.mlab, but not
           as fast as pandas and probably misses some corner cases for each :)
           '''
        
        keynames = list(keynames) if utils.islistlike(keynames) else [keynames]
        keys, index_groups = self.get_index_groups(keynames)
        new_names = [i[-1] for i in fun_fields_name]
        groups = ColumnarRecords([np.fromiter((fun(self[fields][i]) for i in index_groups),
                                              dtype=None, count=len(keys))
                                  for fun, fields, name in fun_fields_name],
                                 names=new_names)
        return join(keys, groups)
    
    def groupby_full(self, keynames, *fun_dtype_fields_name):
        '''Clone of np_utils.rec_groupby_full for a CR
           
           Docs for np_utils.rec_groupby_full:
           A special version of np_groupby for record arrays, somewhat similar
           to the function found in matplotlib.mlab.rec_groupby.
           
           This is basically a wrapper around np_groupy_full that automatically
           generates lambda's like the ones in the np_groupby_full doc string.
           That same call would look like this using rec_grouby_full:
           
           simple_rank = lambda x: np.argsort(x) + 1
           background_subtract = lambda x: x - x.mean()
           simple_normalize = lambda x: x / x.mean()
           
           rec_groupby_full(a, ['m', 'n'],
               (simple_rank,         np.int,   'o',        'rank_o'),
               (simple_rank,         np.int,   ['o', 'p'], 'rank_op'),
               (background_subtract, np.float, 'o',        'bg_sub_o'),
               (simple_normalize,    np.float, 'p',        'norm_p')
           )
           
           
           In general, this function is faster than matplotlib.mlab, but not
           as fast as pandas and probably misses some corner cases for each :)
           '''
        
        keynames = list(keynames) if utils.islistlike(keynames) else [keynames]
        key_cr = self[keynames].ravel()
        keys, index_groups = key_cr.get_index_groups()
        new_names = [i[-1] for i in fun_dtype_fields_name]
        groups = ColumnarRecords([_group_transform(self[fields], index_groups, fun, dtype)
                                  for fun, dtype, fields, name in fun_dtype_fields_name],
                                 names=new_names)
        return join(key_cr, groups)
    
    def tolist(self):
        return [arr.tolist() for arr in self.arrays]
    
    def torecords(self):
        dtype = [(n, d) for n, d in zip(self.names, self.dtypes)]
        return np.rec.fromarrays(self.arrays, dtype=dtype)

def from_recarray(recarray):
    arrays = [recarray[n] for n in recarray.dtype.names]
    return ColumnarRecords(arrays, names=recarray.dtype.names)

def from_records(records, names=None, dtypes=None):
    """A memory-friendly ColumnarRecord constructor that takes
    individual records.
    
    Examples:
    
    columnar_records_from_records([(1, 'a'), (2, 'b')])
    ->
    ColumnarRecords([
      array([1, 2]),
      array(['a', 'b'], 
            dtype='|S1')
     ],
     names=['f0', 'f1'],
     dtypes=[dtype('int64'), dtype('S1')])
    
    columnar_records_from_records([(1, 'a'), (2, 'b')], names=['x', 'y'])
    ->
    ColumnarRecords([
      array([1, 2]),
      array(['a', 'b'], 
            dtype='|S1')
     ],
     names=['x', 'y'],
     dtypes=[dtype('int64'), dtype('S1')])
    """
    n_arrays = len(records[0]) # assume all records have the same length
    if dtypes is None:
        dtypes = [None] * n_arrays
    
    count = len(records)
    arrays = [(np.array([r[i] for r in records],
                        dtype=dtypes[i])
               if dtypes[i] is None or np.dtype(dtypes[i]) == np.object else
               np.fromiter((r[i] for r in records),
                           dtype=dtypes[i], count=count)
              )
              for i in range(n_arrays)]
    return ColumnarRecords(arrays, names=names)

def from_iter(record_iterator, names, dtypes, count):
    '''Create a ColumnarRecords from a record iterator;
       operates without any intermediate memory, but may be slower
       than from_records (this uses a double python for loop).
       
       names, dtypes, and counts MUST be supplied,
       otherwise from_records should be used.'''
    
    arrays = [np.empty(count, dtype=dtype)
              for dtype in dtypes]
    
    for i, r in enumerate(record_iterator):
        for j, rr in enumerate(r):
            arrays[j][i] = rr
    
    return ColumnarRecords(arrays, names=names)

def as_cr(x):
    '''Construct a ColumnarRecords object from:
       * another ColumnarRecords
       * a numpy record array
       * a list of arrays'''
    
    return (x if isinstance(x, ColumnarRecords) else
            from_recarray(x) if _has_records(x) else
            ColumnarRecords(x))

argsort = ColumnarRecords.argsort
sort = ColumnarRecords.sort
groupby = ColumnarRecords.groupby
groupby_full = ColumnarRecords.groupby_full
