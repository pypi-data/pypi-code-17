# Florian P. Bayer
# Sequence.py
from collections import Counter

# NUCLEOTIDE_Alphabet contains all FASTA chars for nucleotides
NUCLEOTIDE_Alphabet = {
    "A": "adenosine",
    "C": "cytidine",
    "G": "guanine",
    "T": "thymidine",
    "U": "uridine",
    "N": "any",  # [A|G|C|T]
    "R": "purine",  # [G|A]
    "Y": "pyrimidine",  # [T|C]
    "K": "keto",  # [G|T]
    "M": "amino",  # [A|C]
    "S": "strong",  # [G|C]
    "W": "weak",  # [A|T]
    "B": "notA",  # [G|T|C]
    "D": "notC",  # [G|A|T]
    "H": "notG",  # [A|C|T]
    "V": "notT",  # [G|C|A]
    "-": "gap",
}

# DNA_Base_Pairing contains all possible hydrogen bonding interactions in FASTA format
DNA_Base_Pairing = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
    "U": "A",  # oxidized Cytosine
    "N": "N",  # [A|G|C|T] <-> [A|G|C|T]
    "R": "Y",  # [A|G] <-> [C|T]
    "Y": "R",  # [C|T] <-> [A|G]
    "K": "M",  # [G|T] <-> [A|C]
    "M": "K",  # [A|C] <-> [G|T]
    "S": "S",  # [C|G] <-> [C|G]
    "W": "W",  # [A|T] <-> [A|T]
    "B": "V",  # [C|G|T] <-> [A|C|G]
    "D": "H",  # [A|G|T] <-> [A|C|T]
    "H": "D",  # [A|C|T] <-> [A|G|T]
    "V": "B",  # [A|C|G] <-> [C|G|T]
    "-": "-",
}

# DNA_Codons contains all DNA triplets in FASTA format
DNA_Codons = {
    'TTT': 'F', 'CCC': 'P', 'AAA': 'K', 'GGG': 'G',
    'TTC': 'F', 'CCT': 'P', 'AAG': 'K', 'GGT': 'G',
    'TTA': 'L', 'CCA': 'P', 'AAC': 'N', 'GGC': 'G',
    'TTG': 'L', 'CCG': 'P', 'AAT': 'N', 'GGA': 'G',
    'TCT': 'S', 'CTC': 'L', 'AGA': 'R', 'GTG': 'V',
    'TCC': 'S', 'CTT': 'L', 'AGG': 'R', 'GTC': 'V',
    'TCA': 'S', 'CTA': 'L', 'AGC': 'S', 'GTT': 'V',
    'TCG': 'S', 'CTG': 'L', 'AGT': 'S', 'GTA': 'V',
    'TAT': 'Y', 'CAC': 'H', 'ACA': 'T', 'GCG': 'A',
    'TAC': 'Y', 'CAT': 'H', 'ACG': 'T', 'GCT': 'A',
    'TAA': '*', 'CAA': 'Q', 'ACC': 'T', 'GCC': 'A',
    'TAG': '*', 'CAG': 'Q', 'ACT': 'T', 'GCA': 'A',
    'TGT': 'C', 'CGC': 'R', 'ATA': 'I', 'GAG': 'E',
    'TGC': 'C', 'CGT': 'R', 'ATC': 'I', 'GAA': 'E',
    'TGA': '*', 'CGA': 'R', 'ATT': 'I', 'GAT': 'D',
    'TGG': 'W', 'CGG': 'R', 'ATG': 'M', 'GAC': 'D',
}

# RNA_Base_Pairing contains all possible hydrogen bonding interactions in FASTA format
RNA_Base_Pairing = {
    "A": "U",
    "C": "G",
    "G": "C",
    "U": "A",
    "T": "A",  # Non standard RNA base: oxidized 5me-Cytosine
    "N": "N",  # [A|G|C|U] <-> [A|G|C|U]
    "R": "Y",  # [A|G] <-> [C|U]
    "Y": "R",  # [C|U] <-> [A|G]
    "K": "M",  # [G|U] <-> [A|C]
    "M": "K",  # [A|C] <-> [G|U]
    "S": "S",  # [C|G] <-> [C|G]
    "W": "W",  # [A|U] <-> [A|U]
    "B": "V",  # [C|G|U] <-> [A|C|G]
    "D": "H",  # [A|G|U] <-> [A|C|U]
    "H": "D",  # [A|C|U] <-> [A|G|U]
    "V": "B",  # [A|C|G] <-> [C|G|U]
    "-": "-",
}

# RNA_Codons contains all DNA triplets in FASTA format
RNA_Codons = {
    'UUU': 'F', 'CCC': 'P', 'AAA': 'K', 'GGG': 'G',
    'UUC': 'F', 'CCU': 'P', 'AAG': 'K', 'GGU': 'G',
    'UUA': 'L', 'CCA': 'P', 'AAC': 'N', 'GGC': 'G',
    'UUG': 'L', 'CCG': 'P', 'AAU': 'N', 'GGA': 'G',
    'UCU': 'S', 'CUC': 'L', 'AGA': 'R', 'GUG': 'V',
    'UCC': 'S', 'CUU': 'L', 'AGG': 'R', 'GUC': 'V',
    'UCA': 'S', 'CUA': 'L', 'AGC': 'S', 'GUU': 'V',
    'UCG': 'S', 'CUG': 'L', 'AGU': 'S', 'GUA': 'V',
    'UAU': 'Y', 'CAC': 'H', 'ACA': 'T', 'GCG': 'A',
    'UAC': 'Y', 'CAU': 'H', 'ACG': 'T', 'GCU': 'A',
    'UAA': '*', 'CAA': 'Q', 'ACC': 'T', 'GCC': 'A',
    'UAG': '*', 'CAG': 'Q', 'ACU': 'T', 'GCA': 'A',
    'UGU': 'C', 'CGC': 'R', 'AUA': 'I', 'GAG': 'E',
    'UGC': 'C', 'CGU': 'R', 'AUC': 'I', 'GAA': 'E',
    'UGA': '*', 'CGA': 'R', 'AUU': 'I', 'GAU': 'D',
    'UGG': 'W', 'CGG': 'R', 'AUG': 'M', 'GAC': 'D',
}

# PROTEIN_Alphabet contains all FATSA chars for amino acids
PROTEIN_Alphabet = {
    "A": "alanine",
    "B": "aspartate/asparagine",
    "C": "cystine",
    "D": "aspartate",
    "E": "glutamate",
    "F": "phenylalanine",
    "G": "glycine",
    "H": "histidine",
    "I": "isoleucine",
    "K": "lysine",
    "L": "leucine",
    "M": "methionine",
    "N": "asparagine",
    "P": "proline",
    "Q": "glutamine",
    "R": "arginine",
    "S": "serine",
    "T": "threonine",
    "U": "selenocysteine",
    "V": "valine",
    "W": "tryptophan",
    "Y": "tyrosine",
    "Z": "glutamate/glutamine",
    "X": "any",
    "*": "translation stop",
    "-": "gap",
}

# Monoisotopic Masses of amino acids in Dalton
AMINOACIDS_Mono_Mass = {
    'A':  71.037114,
    'C': 103.009185,
    'D': 115.026943,
    'E': 129.042593,
    'F': 147.068414,
    'G':  57.021464,
    'H': 137.058912,
    'I': 113.084064,
    'K': 128.094963,
    'L': 113.084064,
    'M': 131.040485,
    'N': 114.042927,
    'P':  97.052764,
    'Q': 128.058578,
    'R': 156.101111,
    'S':  87.032028,
    'T': 101.047679,
    'U': 150.953630,
    'V':  99.068414,
    'W': 186.079313,
    'Y': 163.063332,
    '*': 0,
    '-': 0,
}


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
        def motif_iterator(motif, dna, pos=0):
            while True:
                pos = dna.find(motif, pos)
                if pos == -1:
                    break
                else:
                    yield pos
                pos += next

        # handle overlap to set the next-courser right
        if overlap:
            next = 1
        else:
            next = len(motif)

        # return a list of all starting indexes of motifs in seq
        return [pos for pos in motif_iterator(motif, self.seq, start)]


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
