#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import numpy as np


# complementary DNA
compl_dna = {
    'id': 'compl_dna',
    'src': 'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dst': 'KNDMHCTVGXRAAWYS-.kndmhctvgxraawys',
    'outlier':  '-',
}

# complementary RNA
compl_rna = {
    'id': 'compl_rna',
    'src': 'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dst': 'KNDMHCUVGXRAAWYS-.kndmhcuvgxraawys',
    'outlier':  '-',
}

# reverse complementary DNA
revcompl_dna = {
    'id': 'revcompl_dna',
    'src': 'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dst': 'KNDMHCTVGXRAAWYS-.kndmhctvgxraawys',
    'outlier':  '-',
}

# reverse complementary RNA
revcompl_rna = {
    'id': 'revcompl_rna',
    'src': 'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dst': 'KNDMHCUVGXRAAWYS-.kndmhcuvgxraawys',
    'outlier':  '-',
}


class Transcoder(object):
    _loaded_transcoders = dict()

    def __init__(self, **params):
        self.refarr = self._build_mapping_array(**params)
        self.reverse = params.get('reverse', 'False')
        self._loaded_transcoders[params.get('id')] = self

    @classmethod
    def load(cls, id_):
        try:
            cls._loaded_transcoders[id_]
        except KeyError:
            if not cls._loaded_transcoders:
                cls.load_kb()
            return cls._loaded_transcoders.get(id_)

    @classmethod
    def load_kb(cls):
        cls(**compl_dna)
        cls(**compl_rna)
        cls(**revcompl_dna)
        cls(**revcompl_rna)

    @staticmethod
    def _build_mapping_array(src, dst, outlier='-', **_):
        if not len(src) == len(dst):
            raise ValueError('lengths of src and dst must be equal')

        sarr = np.fromstring(src, dtype='uint8')
        darr = np.fromstring(dst, dtype='uint8')

        arr = np.zeros(256, dtype='uint8')
        arr[sarr] = darr
        arr[arr == 0] = ord(outlier)
        return arr

    def transcode(self, string):
        iarr = np.fromstring(string, dtype='uint8')
        arr = self.refarr[iarr]
        if self.reverse:
            return arr.tostring()[::-1]
        else:
            return arr.tostring()   # returning bytes


