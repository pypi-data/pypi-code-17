'''Tests for ColumnarRecords methods and associated helper functions'''

from builtins import zip
from future.utils import lzip

import numpy as np

from columnar_records import ColumnarRecords, from_records, from_recarray, get_index_groups, groupby, groupby_full

L1 = [[1,2,3,4], ['a', 'b', 'c', 'd']]
L2 = [[1,2,3,4], ['d', 'c', 'b', 'a']]
N2 = ['numbers', 'letters']
L3 = [[1, 1, 2, 2, 3, 3, 4, 4, 4],
     ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
     [float(i) / 9 for i in range(9)]]

cache = {}

def _get_sample_columnar_records():
    '''Build a dummy ColumnarRecords object to test with. Has fields m,n,o,p.
       Cache the result as "cache['sample_cr']" to save time.'''
    if 'sample_cr' in cache:
        cr = cache['sample_cr']
    else:
        l = 10000
        ID = np.arange(l)
        np.random.seed(0)
        m = np.array([['This', 'That'][j] for j in np.random.randint(2, size=l)])
        n = np.random.randint(100, size=l)
        o = np.random.normal(loc=300, scale=100, size=l)
        p = np.random.logistic(0, 20, size=l)
        cr = ColumnarRecords([ID, m, n, o, p], names=list('imnop'))
        cache['sample_cr'] = cr
    return cr

def test_tolist_1():
    cr = ColumnarRecords(L1)
    assert(cr.tolist() == L1)

def test_indexing_1():
    cr = ColumnarRecords(L1)
    assert(cr[0].tolist() == [1, 'a'])

def test_eq_1():
    cr = ColumnarRecords(L1)
    assert(np.array_equal(cr == cr,
           [True]*4))

def test_ne_1():
    cr = ColumnarRecords(L1)
    assert(np.array_equal(cr != cr,
           [False]*4))

def test_array_equal_1():
    cr = ColumnarRecords(L1)
    crB = ColumnarRecords(L1)
    assert(cr.array_equal(
           crB))

def test_slicing_1():
    cr = ColumnarRecords(L1)
    assert(cr[1:3].array_equal(
           [i[1:3] for i in L1]))

def test_slicing_2_with_string():
    cr = ColumnarRecords(L1)
    assert(np.array_equal(cr['f0'],
                          cr.arrays[0]))

def test_slicing_3_with_strings():
    cr = ColumnarRecords(L1)
    assert(cr[['f0', 'f1']].array_equal(
           cr))
    assert(cr['f0', 'f1'].array_equal(
           cr))

def test_slicing_4_reverse():
    cr = ColumnarRecords(L1)
    assert(cr[::-1].array_equal(
           [i[::-1] for i in L1]))

def test_slicing_5():        # really push indexing, etc
    cr = ColumnarRecords(L1)
    assert(cr[None][None][:, :, ::-2][0, 0].array_equal(
           [i[::-2] for i in L1]))

def test_sort_1():
    cr = ColumnarRecords(L1)
    assert(cr[::-1].sort().array_equal(
           cr))

def test_from_records_1():
    cr = ColumnarRecords(L1)
    assert(from_records(lzip(*L1)).array_equal(
           cr))
    
def test_recarray_1():
    cr = ColumnarRecords(L1)
    a = from_recarray(np.rec.fromarrays(L1))
    assert a.array_equal(cr)
    
def test_from_recarray_2():
    cr = ColumnarRecords(L1)
    assert(from_recarray(np.rec.fromarrays(L1)).array_equal(
           cr))

def test_iter_1():
    cr = ColumnarRecords(L1)
    assert([i for i in cr] == lzip(*L1)) # test __iter__
    
    
def test_sort_2():
    cr2 = ColumnarRecords(L2, names=N2)
    assert(cr2.sort().array_equal(
           cr2))

def test_sort_3():
    cr2 = ColumnarRecords(L2, names=N2)
    assert(cr2.sort(['numbers', 'letters']).array_equal(
           cr2))

def test_sort_4():
    cr2 = ColumnarRecords(L2, names=N2)
    assert(cr2.sort(['letters', 'numbers']).array_equal(
           ColumnarRecords([i[::-1] for i in L2], N2)))
    
def test_get_index_groups_1():
    cr3 = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr_a = cr3.get_index_groups(['a'])
    nu_a = get_index_groups(cr3['a'])
    assert(np.array_equal(cr_a[0]['a'], nu_a[0]))
    assert(np.array_equal(cr_a[1], nu_a[1]))
    
def test_get_index_groups_2():
    cr3 = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr_ia = cr3.get_index_groups(['i', 'a'])
    nu_ia = get_index_groups(cr3[['i', 'a']].torecords())
    assert(cr_ia[0].array_equal(from_recarray(nu_ia[0])))
    assert(np.array_equal(cr_ia[1], nu_ia[1]))
    
def test_get_index_groups_3():
    cr3 = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr_ai = cr3.get_index_groups(['a', 'i'])
    nu_ai = get_index_groups(cr3[['a', 'i']].torecords())
    assert(cr_ai[0].array_equal(from_recarray(nu_ai[0])))
    assert(np.array_equal(cr_ai[1], nu_ai[1]))
    
def test_get_index_groups_4():
    cr3 = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr_ia = cr3.get_index_groups(['i', 'a'])
    cr_ai = cr3.get_index_groups(['a', 'i'])
    
    assert(not cr_ia[0].array_equal(
               cr_ai[0]))
    assert(not np.array_equal(cr_ia[1],
                              cr_ai[1]))

def test_groupby_1():
    c = _get_sample_columnar_records()
    g = groupby(c, 'n', (np.max, 'o', 'max_o'))
    assert g.shape == (100,)
    assert g.names == ['n', 'max_o']
    assert g.dtypes == [np.int, np.float]
    assert np.all(g['n'] == np.arange(100))
    assert np.all(g['max_o'] > 450)

def test_groupby_2():
    c = _get_sample_columnar_records()
    g = groupby(c, 'n', (np.max, 'o', 'max_o'),
                           (np.min, 'o', 'min_o'))
    assert g['max_o'][0] != g['min_o'][0]

def test_groupby_3():
    c = _get_sample_columnar_records()
    dtype1 = c.dtypes[1] # Either '<S4' or '<U4'
    g = groupby(c, ['m', 'n'], (np.mean, 'o', 'mean_o'),
                               (np.std, 'o', 'std_o'),
                               (np.min, 'p', 'min_p'))
    assert g.shape == (200,)
    assert g.names == ['m', 'n', 'mean_o', 'std_o', 'min_p']
    assert g.dtypes == [dtype1, '<i8', '<f8', '<f8', '<f8']

def test_groupby_4():
    c = _get_sample_columnar_records()
    dtype1 = c.dtypes[1] # Either '<S4' or '<U4'
    
    def compute_some_thing(x):
        o, p = x['o'], x['p']
        return np.mean(o) / np.std(o) * np.min(p)
    
    g = groupby(c, ['m', 'n'], (compute_some_thing, ['o', 'p'], 'its_complicated'))
    assert g.shape == (200,)
    assert g.names == ['m', 'n', 'its_complicated']
    assert g.dtypes == [dtype1, '<i8', '<f8']


def test_groupby_5():
    c = _get_sample_columnar_records()
    def compute_some_thing(x):
        o, p = x['o'], x['p']
        return np.mean(o) / np.std(o) * np.min(p)
    
    g_mn = groupby(c, ['m', 'n'], (compute_some_thing, ['o', 'p'], 'its_complicated'))
    g_nm = groupby(c, ['n', 'm'], (compute_some_thing, ['o', 'p'], 'its_complicated'))
    
    assert not np.array_equal(g_mn, g_nm)

def test_groupby_full_1():
    c = _get_sample_columnar_records()
    simple_rank = lambda x: x.argsort() + 1
    background_subtract = lambda x: x - x.mean()
    simple_normalize = lambda x: x / x.mean()
    
    r = groupby_full(c, ['m', 'n'],
        #(simple_rank,         np.int,   'o',        'rank_o'),
        #(simple_rank,         np.int,   ['o', 'p'], 'rank_op'),
        (background_subtract, np.float, 'o',        'bg_sub_o'),
        (simple_normalize,    np.float, 'p',        'norm_p')
    )
    assert(np.isclose(r['bg_sub_o'].mean(), 0))
    assert(np.isclose(r['norm_p'].mean(), 1))
    assert(not np.array_equal(r['bg_sub_o'], background_subtract(c['o'])))
    assert(not np.array_equal(r['norm_p'], simple_normalize(c['p'])))

def test_setslice_1():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    insert = ColumnarRecords([i[:2] for i in L3], names=['i', 'a', 'f'])
    cr[1:3] = insert
    assert(cr[1].array_equal(cr[0]))


def test_setitem_1():
    cr = ColumnarRecords(L1)
    cr['f0'] = [5,6,7,8]
    assert(cr.array_equal(
           [[5,6,7,8], L1[1]]))

def test_setitem_2():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr['f', 'a'] = [[float(i) for i in range(9)], list('thereare9')]
    assert(cr.array_equal(
           ColumnarRecords([L3[0], list('thereare9'), np.arange(9)],
                           names=['i', 'a', 'f'])))

def test_setitem_3():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr['a', 'f'] = ColumnarRecords([np.arange(9), list('thereare9')], names=['f', 'a'])
    assert(cr.array_equal(
           ColumnarRecords([L3[0], list('thereare9'), np.arange(9)],
                           names=['i', 'a', 'f'])))

def test_setitem_4():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr[:4] = cr[-4:]
    assert(cr[:4].array_equal(
           cr[-4:]))

def test_setitem_5():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr[4] = cr[0]
    assert(cr[4].array_equal(
           cr[0]))

def test_setitem_6():
    cr = ColumnarRecords(L3, names=['i', 'a', 'f'])
    cr[[1, 4]] = cr[[0, 2]]
    assert(cr[[1, 4]].array_equal(
           cr[[0, 2]]))

if __name__ == '__main__':
    test_tolist_1()
    test_indexing_1()
    test_eq_1()
    test_ne_1()
    test_array_equal_1()
    test_slicing_1()
    test_slicing_2_with_string()
    test_slicing_3_with_strings()
    test_slicing_4_reverse()
    test_slicing_5()
    test_sort_1()
    test_from_records_1()
    test_recarray_1()
    test_from_recarray_2()
    test_iter_1()
    test_sort_2()
    test_sort_3()
    test_sort_4()
    test_get_index_groups_1()
    test_get_index_groups_2()
    test_get_index_groups_3()
    test_get_index_groups_4()
    test_groupby_1()
    test_groupby_2()
    test_groupby_3()
    test_groupby_4()
    test_groupby_5()
    test_groupby_full_1()
    test_setslice_1()
    test_setitem_1()
    test_setitem_2()
    test_setitem_3()
    test_setitem_4()
    test_setitem_5()
    test_setitem_6()

    
    
