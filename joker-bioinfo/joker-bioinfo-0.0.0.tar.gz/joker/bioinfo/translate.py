#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import numpy as np
import re
import os


class Translator(object):
    def __init__(self, mapping):
        """
        :param mapping: a dict which maps condons to AAs
        """
        condons = [c.upper() for c in mapping]
        condons.sort()
        packarr = self._gen_packarr(''.join(condons))

        # max(packarr) < 64 (2**6)
        self.refarr = np.empty(128, dtype='uint8')

        # refarr[packed_value] = amino_acid
        self.refarr[packarr] = [ord(mapping[c]) for c in condons]
        self.refarr[64:] = ord('X')

    @classmethod
    def _gen_packarr(cls, string):
        """
        A   0100 0001
        C   0100 0011
        G   0100 0111
        T   0101 0100
        :param string: containing only upper-case letters and len(string) % 3 == 0
        :return:
        """
        arr = np.fromstring(string, dtype='uint8')
        arr[arr == ord('T')] = 0
        arr[arr == ord('A')] = 1
        arr[arr == ord('G')] = 2
        arr[arr == ord('C')] = 3

        arr[arr > 3] = int('01010101', base=2)

        arr.shape = -1, 3

        # mask out unwanted bits
        arr <<= np.array([0, 2, 4], dtype='uint8')

        # 50x faster than arr.sum(axis=1)
        packarr = arr[:, 0] | arr[:, 1] | arr[:, 2]
        return packarr

    def translate(self, seq):
        """
        Translate DNA seq to protein seq
        :param seq: a string whose length is a multiple of 3
        :return: a string (bytes)
        """
        packarr = self._gen_packarr(seq)
        arr = self.refarr[packarr]
        return arr.tostring()


class CodonTable(object):
    _loaded_tables = dict()
    _ncbi_standard_transl = {
        'tid': 1,
        'init': {'TTG', 'CTG', 'ATG'},
        'stop': {'TAA', 'TAG', 'TGA'},
        'mapping': {
            'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S',
            'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y',
            'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
            'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
            'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I',
            'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 'ACC': 'T',
            'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K',
            'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
            'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
            'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D',
            'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
            'GGG': 'G', 'TAA': '*', 'TAG': '*', 'TGA': '*',
        },
    }

    def __init__(self, mapping, init, stop, **kwargs):
        self.mapping = mapping
        self.init = init
        self.stop = stop
        self._translator = Translator(mapping)
        self._loaded_tables[kwargs.get('tid')] = self

    @classmethod
    def load(cls, tid=1):
        try:
            return cls._loaded_tables[tid]
        except KeyError:
            if tid == 0:
                return cls(**cls._ncbi_standard_transl)
            if len(cls._loaded_tables) < 2:
                cls.load_kb()
                try:
                    return cls._loaded_tables[tid]
                except KeyError:
                    pass
            raise KeyError('cannot find transl table {}'.format(tid))

    @classmethod
    def load_kb(cls):
        import joker.bioinfo
        path = os.path.dirname(joker.bioinfo.__file__)
        path = os.path.join(path, 'kb/transl_tabs.txt')
        for text in open(path).read().split('==SEPARATOR=='):
            transl_dic = cls.parse_ncbi_format(text)
            cls._loaded_tables[transl_dic.get('id')] = cls(**transl_dic)

    @classmethod
    def from_ncbi_format(cls, text):
        return cls(**cls.parse_ncbi_format(text))

    @staticmethod
    def parse_ncbi_format(text):
        """
        example input::
        # 1. The Standard Code (transl_table=1) 
        AAs     = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
        Starts  = ---M------**--*----M---------------M----------------------------
        Base1   = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
        Base2   = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
        Base3   = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG
       
        example output::
        {
            'tid': 1,
            'title': '1. The Standard Code',
            'init': {'TTG', 'CTG', 'ATG'},
            'stop': {'TAA', 'TAG', 'TGA'},
            'mapping': {
                'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S',
                'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y',
                'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
                'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
                'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
                'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I',
                'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 'ACC': 'T',
                'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K',
                'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
                'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
                'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D',
                'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
                'GGG': 'G', 'TAA': '*', 'TAG': '*', 'TGA': '*',
            },
        }    
        """
        d = dict()
        ret = dict(id=0, title='')
        title_regex = re.compile(r'#\s*([^()]+)\(transl_table=(\d+)\)')
        mat = title_regex.match(text)
        if mat:
            title, tabid = mat.groups()
            ret['tid'] = int(tabid)
            ret['title'] = title.strip()

        regex = re.compile(r'(\w+)\s*=\s*([\w*-]+)$')
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            mat = regex.match(line)
            if not mat:
                continue
            k, v = mat.groups()
            d[k.lower()] = v
        # print(d)
        codons = [''.join(t) for t in zip(d['base1'], d['base2'], d['base3'])]
        ret['mapping'] = dict(zip(codons, d['aas']))
        ret['stop'] = {k for (k, v) in zip(codons, d['starts']) if v == '*'}
        ret['init'] = {k for (k, v) in zip(codons, d['starts']) if v == 'M'}
        return ret

    def translate(self, seq, trim_aster=False):
        p = self._translator.translate(seq).decode()
        if trim_aster and p.endswith('*'):
            p = p[:-1]
        return p


CodonTable.load(0)
