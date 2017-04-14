# (c) 2017, Florian P. Bayer <f.bayer@tum.de>
#
# Sequence.py is part of the PyOmics project.
# It contains all kinds of Sequence objects that provide useful functionality.

# Import intern modules
from .constants import *

# Import standard modules
import re
from collections import Counter



class _Sequence(object):
    """
    The base class of a Sequence. 
    A Sequence is an immutable string-like object.
    The identification of a Sequence has dict-like functionality.
    """
    alphabet = set(NUCLEOTIDE_Alphabet) | set(PROTEIN_Alphabet)

    def __init__(self, sequence, **identifiers):
        self.seq = sequence
        self.id = identifiers
        self.counter = None

    # Object representations
    def __repr__(self):
        return self.seq

    def __str__(self):
        if len(self.seq) >= 23:
            return self.seq[:10] + '...' + self.seq[-10:]
        return self.seq

    # Dictionary-like access for identifier access
    def __setitem__(self, key, value):
        self.id[key] = value

    def __delitem__(self, key):
        del self.id[key]

    def __missing__(self, key):
        return None

    def __getitem__(self, key):
        if key in self.id:
            return self.id[key]
        else:
            return self.__missing__(key)

    # Equality is given if the sequence is equal and objects are of the same class
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.seq == other.seq

    def __ne__(self, other):
        if self.__class__ != other.__class__:
            return True
        return self.seq != other.seq

    # Changes upon the underlying sequence implies a new sequence object
    # Operations are only possible for certain object combinations
    def __add__(self, other):
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} + {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __radd__(self, other):
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} + {}".format(other.__class__.__name__, self.__class__.__name__, )
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __iadd__(self, other):
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} =+ {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __mul__(self, other):
        if not isinstance(other, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} * {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(other * self.seq)

    def __rmul__(self, other):
        if not isinstance(other, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} * {}".format(other.__class__.__name__, self.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(other * self.seq)

    def __imul__(self, other):
        if not isinstance(other, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} =* {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(other * self.seq)

    # General functions that focus on sequence characteristics
    def __len__(self):
        return len(self.seq)

    def __contains__(self, motif):
        return motif.seq in self.seq

    def __iter__(self):
        for char in self.seq:
            yield char

    def count(self):
        if not self.counter:
            self.counter = Counter(self.seq)
        return self.counter

    def find(self, motif, overlap=True, start=0):
        # use an iterator for each next str.find index (fast!!)
        def motif_iterator(inner_motif, dna, start_at=0, shift_to=1):
            while True:
                found_at = dna.find(inner_motif, start_at)
                if found_at == -1:
                    break
                else:
                    yield found_at
                start_at = found_at + shift_to

        # handle overlap to set the shift_to courser to the right next position
        # return a list of all found_at indexes of a motif's beginning in seq
        if overlap:
            return [pos for pos in motif_iterator(motif, self.seq, start, shift_to=1)]
        else:
            return [pos for pos in motif_iterator(motif, self.seq, start, shift_to=len(motif))]

    def digested(self, by, sort=True, as_str=False):
        # a sorted list of all unique fragment strings
        fragments = list({*re.split(by, self.seq)})

        # if sorted is True: sort the fragments by length in reversed order
        if sort:
            fragments = sorted(fragments, key=len, reverse=True)

        # if as string is True: return the fragments simply as strings; else: as *Sequence objects
        if as_str:
            return fragments
        return [self.__class__(f) for f in fragments]


class _NucleotideSequence(_Sequence):
    """
    A hidden base class for DNA and RNA Sequences.
    """
    alphabet = NUCLEOTIDE_Alphabet

    def gc(self):
        return (self.seq.count('C') + self.seq.count('G')) / len(self.seq)

    def reverse(self):
        return self.__class__(self.seq[::-1], **self.id)

    def complement(self, base_pairing):
        table = str.maketrans(base_pairing)
        return self.__class__(self.seq.translate(table), **self.id)

    def reverse_complement(self, base_pairing):
        table = str.maketrans(base_pairing)
        return self.__class__(self.seq.translate(table)[::-1], **self.id)

    def translate(self, codon, from_start=False):
        start = -1

        # start from the beginning
        if from_start:
            start = 0

        # start with first occurring start codon for Met: AUG or ATG
        else:
            if isinstance(self, DNASequence):
                start = self.seq.find('ATG')
            if isinstance(self, RNASequence):
                start = self.seq.find('AUG')
            if start == -1:
                return ProteinSequence('')

        # only iterate to the last possible codon
        end = len(self.seq) - (len(self.seq) - start) % 3

        protein_seq = ''
        for i in range(start, end, 3):
            # map the triplet to amino acid sequence
            amino_acid = codon[self.seq[i:i + 3]]
            # if a stop codon has been reached: break
            if amino_acid == '*':
                break
            protein_seq += amino_acid
        return ProteinSequence(protein_seq, **self.id)


class ProteinSequence(_Sequence):
    """
    A Protein Sequence
    """
    alphabet = PROTEIN_Alphabet

    def mass(self, ndigits=5):
        # The weight of an empty sequence is 0 Dalton
        if len(self) == 0:
            return 0

        # Refuse to calculate the weight when B or Z is present in the sequence
        if set(self.seq) & set('BZ'):
            return None

        # Calculate the mass
        h2o = 18.010565  # Monoisotopic mass of terminal water in Dalton
        totalmass = sum([AMINOACIDS_Mono_Mass[aminoacid] for aminoacid in self.seq]) + h2o
        return round(totalmass, ndigits)


class DNASequence(_NucleotideSequence):
    """
    A DNA Sequence
    """
    def complement(self, **kwargs):
        return super(DNASequence, self).complement(DNA_Base_Pairing)

    def reverse_complement(self, **kwargs):
        return super(DNASequence, self).reverse_complement(DNA_Base_Pairing)

    def translate(self, **kwargs):
        return super(DNASequence, self).translate(DNA_Codons, **kwargs)

    def transcribe(self):
        return RNASequence(self.seq.replace("T", "U"), **self.id)


class RNASequence(_NucleotideSequence):
    """
    A RNA Sequence
    """
    def complement(self, **kwargs):
        return super(RNASequence, self).complement(RNA_Base_Pairing)

    def reverse_complement(self, **kwargs):
        return super(RNASequence, self).reverse_complement(RNA_Base_Pairing)

    def translate(self, **kwargs):
        return super(RNASequence, self).translate(RNA_Codons, **kwargs)

    def reverse_transcribe(self):
        return DNASequence(self.seq.replace("U", "T"), **self.id)


if __name__ == '__main__':
    pass
