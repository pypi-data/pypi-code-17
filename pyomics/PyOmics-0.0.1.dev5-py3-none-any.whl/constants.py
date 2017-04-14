# (c) 2017, Florian P. Bayer <f.bayer@tum.de>
#
# conctants.py is part of the PyOmics project.
# It contains all useful constants that might be used across all PyOmics' modules.

import re

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

# Precompiled regex cleavage patterns to digest a protein sequence
PROTEIN_Cleavage = {
    # Arg-C :: C-terminal side of R :: NOT if P is C-term to R
    'Arg-C': re.compile(r'((?<=[R]).*?[R](?![P]))'),
    # Lys C :: C-terminal side of K
    'Lys-C': re.compile(r'((?<=[K]).*?[K])'),
    # Trypsin :: C-terminal side of K or R :: NOT if P is C-term to K or R
    'Trypsin': re.compile(r'((?<=[RK]).*?[RK](?![P]))'),
    # Cyanogen bromide cleavage :: C-terminal side of M
    'CNBr': re.compile(r'((?<=[M]).*?[M])'),
    # Chymotrypsin :: C-terminal side of F, L, M, W, Y :: NOT if P is N-term to Y, NOT if P is C-term to F, L, M, W, Y,
    'Chymotrypsin': re.compile(r'((?<=[FLMWY]).*?(?:(?<![P])[Y](?![P])|[FLMW](?![P])))'),
    # Pepsin (pH > 2) :: C-terminal side of F, L, W, Y, A, E, Q
    'Pepsin-high-pH': re.compile(r'((?<=[FLWYAEQ]).*?[FLWYAEQ])'),
    # Pepsin proteinase (pH = 1.3) :: C-terminal side of F, L
    'Pepsin-low-pH': re.compile(r'((?<=[FL]).*?[FL])'),
    # Proteinase K :: C-terminal side of A, F, Y, W, L, I, V
    'Proteinase-K': re.compile(r'((?<=[AFYWLIV]).*?[AFYWLIV])'),
    # Lys N :: C-terminal side of K
    'Lys-N': re.compile(r'([K].*?(?=[K]))'),
    # Asp N Proteinase :: N-terminal side of D
    'Asp-N': re.compile(r'([D].*?(?=[D]))'),
    # Thermolysin :: N-terminal side of A, F, I, L, M, V :: NOT if D or E is N-term to A, F, I, L, M, V ;
    # NOT if P is C-term to A, F, I, L, M, V
    'Thermolysin': re.compile(r'([AFILMV].*?(?=(?<![DE])[AFILMV](?![P])))'),
    # Glu C (bicarbonate) :: C-terminal side of E :: NOT if P is C-term to E, NOT if E is C-term to E
    'Glu-C': re.compile(r'((?<=[E]).*?[E](?![PE]))'),
    # LysargiNase :: N-terminal side of K, R
    'LysargiNase': re.compile(r'([KR].*?(?=[KR]))'),
    # microwave-assisted acid hydrolysis (MAAH) :: C-terminal side of D
    'MAAH': re.compile(r'((?<=[D]).*?[D])')
}
