# (c) 2017, Florian P. Bayer <f.bayer@tum.de>
#
# constants.py is part of the PyOmics project.
# It contains all useful constants that might be used across all PyOmics' modules.

import re

# NUCLEOTIDE_Alphabet contains all FASTA chars for nucleotides
# https://en.wikipedia.org/wiki/Nucleic_acid_notation
NUCLEOTIDE_Alphabet = {
    "A": "adenine",
    "C": "cytosine",
    "G": "guanine",
    "T": "thymine",
    "U": "uracil",
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
# https://en.wikipedia.org/wiki/DNA_codon_table
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
# https://en.wikipedia.org/wiki/Genetic_code#RNA_codon_table
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

# PROTEIN_Alphabet contains all FASTA chars for amino acids
# https://en.wikipedia.org/wiki/Amino_acid#Table_of_standard_amino_acid_abbreviations_and_properties
PROTEIN_Alphabet = {
    "A": "alanine",
    "B": "aspartate/asparagine",
    "C": "cysteine",
    "D": "aspartate",
    "E": "glutamate",
    "F": "phenylalanine",
    "G": "glycine",
    "H": "histidine",
    "I": "isoleucine",
    "J": "leucine/isoleucine",
    "K": "lysine",
    "L": "leucine",
    "M": "methionine",
    "N": "asparagine",
    "O": "pyrrolysine",
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

# Monoisotopic Masses of amino acid side chain residues in Dalton
# http://www.matrixscience.com/help/aa_help.html
AMINOACIDS_Mono_Mass = {
    'A':  71.037114,
    'C': 103.009185,
    'D': 115.026943,
    'E': 129.042593,
    'F': 147.068414,
    'G':  57.021464,
    'H': 137.058912,
    'I': 113.084064,
    'J': 113.084064,
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

# pka values from side chains from various sources
AMINOACIDS_Pkas = {
    'EMBOSS': {'NH2': 8.60, 'COOH': 3.60, 'C': 8.50, 'D': 3.90, 'E': 4.10, 'H': 6.50, 'K': 10.80, 'R': 12.50,
               'Y': 10.10},
    'DTASelect': {'NH2': 8.00, 'COOH': 3.10, 'C': 8.50, 'D': 4.40, 'E': 4.40, 'H': 6.50, 'K': 10.00, 'R': 12.00,
                  'Y': 10.00},
    'Solomon': {'NH2': 9.60, 'COOH': 2.40, 'C': 8.30, 'D': 3.90, 'E': 4.30, 'H': 6.00, 'K': 10.50, 'R': 12.50,
                'Y': 10.10},
    'Sillero': {'NH2': 8.20, 'COOH': 3.20, 'C': 9.00, 'D': 4.00, 'E': 4.50, 'H': 6.40, 'K': 10.40, 'R': 12.00,
                'Y': 10.00},
    'Rodwell': {'NH2': 8.00, 'COOH': 3.10, 'C': 8.33, 'D': 3.68, 'E': 4.25, 'H': 6.00, 'K': 11.50, 'R': 11.50,
                'Y': 10.07},
    'Wikipedia': {'NH2': 8.20, 'COOH': 3.65, 'C': 8.18, 'D': 3.90, 'E': 4.07, 'H': 6.04, 'K': 10.54, 'R': 12.48,
                  'Y': 10.46},
    'Lehninger': {'NH2': 9.69, 'COOH': 2.34, 'C': 8.33, 'D': 3.86, 'E': 4.25, 'H': 6.00, 'K': 10.50, 'R': 12.40,
                  'Y': 10.00},
    'Grimsley': {'NH2': 7.70, 'COOH': 3.30, 'C': 6.80, 'D': 3.50, 'E': 4.20, 'H': 6.60, 'K': 10.50, 'R': 12.04,
                 'Y': 10.30},
}

# Precompiled regex cleavage patterns to digest a protein sequence
# Basic structure for C-terminal fragmentation: ( (?<=[regex])? .*?    [regex]  (?![regex])            )
# Basic structure for N-terminal fragmentation: (     [regex]   .*? (?=[regex])            | [regex].* )
# Using capture groups to get captured match output from re.split
PROTEIN_Cleavage = {
    # Arg-C :: C-terminal side of R :: NOT if P is C-term to R
    'Arg-C': re.compile(r'((?<=[R])?.*?[R](?![P]))'),
    # Lys C :: C-terminal side of K
    'Lys-C': re.compile(r'((?<=[K])?.*?[K])'),
    # Trypsin :: C-terminal side of K or R :: NOT if P is C-term to K or R
    'Trypsin': re.compile(r'((?<=[RK])?.*?[RK](?![P]))'),
    # Cyanogen bromide cleavage :: C-terminal side of M
    'CNBr': re.compile(r'((?<=[M])?.*?[M])'),
    # Chymotrypsin :: C-terminal side of F, L, M, W, Y :: NOT if P is N-term to Y, NOT if P is C-term to F, L, M, W, Y,
    'Chymotrypsin': re.compile(r'((?<=[FLMWY])?.*?(?:(?<![P])[Y](?![P])|[FLMW](?![P])))'),
    # Pepsin (pH > 2) :: C-terminal side of F, L, W, Y, A, E, Q
    'Pepsin-high-pH': re.compile(r'((?<=[FLWYAEQ])?.*?[FLWYAEQ])'),
    # Pepsin proteinase (pH = 1.3) :: C-terminal side of F, L
    'Pepsin-low-pH': re.compile(r'((?<=[FL])?.*?[FL])'),
    # Proteinase K :: C-terminal side of A, F, Y, W, L, I, V
    'Proteinase-K': re.compile(r'((?<=[AFYWLIV])?.*?[AFYWLIV])'),
    # Lys N :: C-terminal side of K
    'Lys-N': re.compile(r'([K].*?(?=[K])|[K].*)'),
    # Asp N Proteinase :: N-terminal side of D
    'Asp-N': re.compile(r'([D].*?(?=[D])|[D].*)'),
    # Thermolysin :: N-terminal side of A, F, I, L, M, V :: NOT if D or E is N-term to A, F, I, L, M, V ;
    # NOT if P is C-term to A, F, I, L, M, V
    'Thermolysin': re.compile(r'([AFILMV].*?(?=(?<![DE])[AFILMV](?![P]))|[AFILMV](?![P]).*)'),
    # Glu C (bicarbonate) :: C-terminal side of E :: NOT if P is C-term to E, NOT if E is C-term to E
    'Glu-C': re.compile(r'((?<=[E])?.*?[E](?![PE]))'),
    # LysargiNase :: N-terminal side of K, R
    'LysargiNase': re.compile(r'([KR].*?(?=[KR])|[KR].*)'),
    # microwave-assisted acid hydrolysis (MAAH) :: C-terminal side of D
    'MAAH': re.compile(r'((?<=[D])?.*?[D])')
}

# A collection of common restriction enzymes with their recognition site. The cut is denoted by 5'..."/"...3' .
# Collected from various sources. Only the HF labeled enzymes are tested to be correct.
# Please always check whether the fragments look as expected.If not, please report it !!
# Your contribution makes PyOmics more reliable and stable. Thank You !!
# To use Restriction Enzymes on Sequences, they get compiled into a regex format using the _to_regex function
RESTRICTION_Enzymes = {
    'AatI': 'AGG/CCT',
    'AatII': 'GACGT/C',
    'Acc65I': 'G/GTACC',
    'AccI': 'GT/MKAC',
    'AccIII': 'T/CCGGA',
    'AciI': 'C/CGC',
    'AclI': 'AA/CGTT',
    'AcsI': 'R/AATTY',
    'AcuI': 'CTGAAGNNNNNNNNNNNNNNNN/',
    'AcyI': 'GR/CGYC',
    'AfeI': 'AGC/GCT',
    'AflI': 'G/GWCC',
    'AflII': 'C/TTAAG',
    'AflIII': 'A/CRYGT',
    'AgeI': 'A/CCGGT',
    'AgeI-HF': 'A/CCGGT',
    'AhaII': 'GR/CGYC',
    'AhaIII': 'TTT/AAA',
    'AhdI': 'GACNNN/NNGTC',
    'AleI': 'CACNN/NNGTG',
    'AluI': 'AG/CT',
    'Alw44I': 'G/TGCAC',
    'AlwI': 'GGATCNNNN/N',
    'AlwNI': 'CAGNNN/CTG',
    'AocI': 'CC/TNAGG',
    'AosI': 'TGC/GCA',
    'ApaI': 'GGGCC/C',
    'ApaLI': 'G/TGCAC',
    'ApeKI': 'G/CWGC',
    'ApoI': 'R/AATTY',
    'ApoI-HF': 'R/AATTY',
    'ApyI': '/CCWGG',
    'AscI': 'GG/CGCGCC',
    'AseI': 'AT/TAAT',
    'AsiSI': 'GCGAT/CGC',
    'AsnI': 'AT/TAAT',
    'Asp700': 'GAANN/NNTTC',
    'Asp718': 'G/GTACC',
    'AspEI': 'GACNNN/NNGTC',
    'AspHI': 'GWGCW/C',
    'AspI': 'GACN/NNGTC',
    'AsuII': 'TT/CGAA',
    'AvaI': 'C/YCGRG',
    'AvaII': 'G/GWCC',
    'AviII': 'TGC/GCA',
    'AvrII': 'C/CTAGG',
    'BaeGI': 'GKGCM/C',
    'BalI': 'TGG/CCA',
    'BamHI': 'G/GATCC',
    'BamHI-HF': 'G/GATCC',
    'BanI': 'G/GYRCC',
    'BanII': 'GRGCY/C',
    'BbrPI': 'CAC/GTG',
    'BbsI': 'GAAGACNN/NNNN',
    'BbsI-HF': 'GAAGACNN/NNNN',
    'BbvCI': 'CC/TCAGC',
    'BbvI': 'GCAGCNNNNNNNN/NNNN',
    'BccI': 'CCATCNNNN/N',
    'BceAI': 'ACGGCNNNNNNNNNNNN/NN',
    'BciVI': 'GTATCCNNNNNN/',
    'BclI': 'T/GATCA',
    'BcoDI': 'GTCTCN/NNNN',
    'BfaI': 'C/TAG',
    'BfrI': 'C/TTAAG',
    'BfuAI': 'ACCTGCNNNN/NNNN',
    'BfuCI': '/GATC',
    'BglI': 'GCCNNNN/NGGC',
    'BglII': 'A/GATCT',
    'BinI': 'C/CTAGG',
    'BlpI': 'GC/TNAGC',
    'Bme1580I': 'GKGCM/C',
    'BmgBI': 'CAC/GTC',
    'BmrI': 'ACTGGGNNNNN/',
    'BmtI': 'GCTAG/C',
    'BmtI-HF': 'GCTAG/C',
    'BmyI': 'GDGCH/C',
    'BpmI': 'CTGGAGNNNNNNNNNNNNNNNN/',
    'Bpu10I': 'CC/TNAGC',
    'Bpu1102I': 'GC/TNAGC',
    'BpuEI': 'CTTGAGNNNNNNNNNNNNNNNN/',
    'BsaAI': 'YAC/GTR',
    'BsaBI': 'GATNN/NNATC',
    'BsaHI': 'GR/CGYC',
    'BsaI': 'GGTCTCN/NNNN',
    'BsaI-HF': 'GGTCTCN/NNNN',
    'BsaJI': 'C/CNNGG',
    'BsaWI': 'W/CCGGW',
    'BseAI': 'T/CCGGA',
    'BsePI': 'G/CGCGC',
    'BseRI': 'GAGGAGNNNNNNNNNN/',
    'BseYI': 'C/CCAGC',
    'BsgI': 'GTGCAGNNNNNNNNNNNNNNNN/',
    'BsiEI': 'CGRY/CG',
    'BsiHKAI': 'GWGCW/C',
    'BsiWI': 'C/GTACG',
    'BsiWI-HF': 'C/GTACG',
    'BsiYI': 'CCNNNNN/NNGG',
    'BslI': 'CCNNNNN/NNGG',
    'BsmAI': 'GTCTCN/NNNN',
    'BsmBI': 'CGTCTCN/NNNN',
    'BsmFI': 'GGGACNNNNNNNNNN/NNNN',
    'BsmI': 'GAATGCN/',
    'BsoBI': 'C/YCGRG',
    'Bsp1286I': 'GDGCH/C',
    'Bsp1407I': 'T/GTACA',
    'BspCNI': 'CTCAGNNNNNNNNN/',
    'BspDI': 'AT/CGAT',
    'BspEI': 'T/CCGGA',
    'BspHI': 'T/CATGA',
    'BspLU11I': 'A/CATGT',
    'BspMI': 'ACCTGCNNNN/NNNN',
    'BspQI': 'GCTCTTCN/NNN',
    'BsrBI': 'CCG/CTC',
    'BsrDI': 'GCAATGNN/',
    'BsrFI': 'R/CCGGY',
    'BsrGI': 'T/GTACA',
    'BsrGI-HF': 'T/GTACA',
    'BsrI': 'ACTGGN/',
    'BssGI': 'CCANNNNN/NTGG',
    'BssHII': 'G/CGCGC',
    'BssKI': '/CCNGG',
    'BssSI': 'C/ACGAG',
    'Bst1107I': 'GTA/TAC',
    'BstAPI': 'GCANNNN/NTGC',
    'BstBI': 'TT/CGAA',
    'BstEII': 'G/GTNACC',
    'BstEII-HF': 'G/GTNACC',
    'BstNI': 'CC/WGG',
    'BstUI': 'CG/CG',
    'BstXI': 'CCANNNNN/NTGG',
    'BstYI': 'R/GATCY',
    'BstZ17I': 'GTA/TAC',
    'BstZ17I-HF': 'GTA/TAC',
    'Bsu36I': 'CC/TNAGG',
    'BtgI': 'C/CRYGG',
    'BtgZI': 'GCGATGNNNNNNNNNN/NNNN',
    'BtsCI': 'GGATGNN/',
    'BtsI': 'GCAGTGNN/',
    'BtsIMutI': 'CAGTGNN/',
    'Cac8I': 'GCN/NGC',
    'CelII': 'GC/TNAGC',
    'CfoI': 'GCG/C',
    'Cfr10I': 'R/CCGGY',
    'CfrI': 'Y/GGCCR',
    'ClaI': 'AT/CGAT',
    'CviAII': 'C/ATG',
    'CviKI-1': 'RG/CY',
    'CviQI': 'G/TAC',
    'DdeI': 'C/TNAG',
    'DpnI': 'GA/TC',
    'DpnII': '/GATC',
    'DraI': 'TTT/AAA',
    'DraII': 'RG/GNCCY',
    'DraIII': 'CACNNN/GTG',
    'DraIII-HF': 'CACNNN/GTG',
    'DrdI': 'GACNNNN/NNGTC',
    'DsaI': 'C/CRYGG',
    'EaeI': 'Y/GGCCR',
    'EagI': 'C/GGCCG',
    'EagI-HF': 'C/GGCCG',
    'Eam1105I': 'GACNNN/NNGTC',
    'EarI': 'CTCTTCN/NNNN',
    'EciI': 'GGCGGANNNNNNNNNNN/',
    'Ecl136II': 'GAG/CTC',
    'EclXI': 'C/GGCCG',
    'Eco47III': 'AGC/GCT',
    'Eco53kI': 'GAG/CTC',
    'EcoNI': 'CCTNN/NNNAGG',
    'EcoO109I': 'RG/GNCCY',
    'EcoRI': 'G/AATTC',
    'EcoRI-HF': 'G/AATTC',
    'EcoRII': '/CCWGG',
    'EcoRV': 'GAT/ATC',
    'EcoRV-HF': 'GAT/ATC',
    'EspI': 'GC/TNAGC',
    'FatI': '/CATG',
    'FauI': 'CCCGCNNNN/NN',
    'Fnu4HI': 'GC/NGC',
    'FnuDII': 'CG/CG',
    'FokI': 'GGATGNNNNNNNNN/NNNN',
    'FseI': 'GGCCGG/CC',
    'FspEI': 'CCNNNNNNNNNNNN/NNNN',
    'FspI': 'TGC/GCA',
    'HaeII': 'RGCGC/Y',
    'HaeIII': 'GG/CC',
    'HgaI': 'GACGCNNNNN/NNNNN',
    'HgiAI': 'GWGCW/C',
    'HhaI': 'GCG/C',
    'HinP1I': 'G/CGC',
    'HinPI': 'G/CGC',
    'HincII': 'GTY/RAC',
    'HindII': 'GTY/RAC',
    'HindIII': 'A/AGCTT',
    'HindIII-HF': 'A/AGCTT',
    'HinfI': 'G/ANTC',
    'HpaI': 'GTT/AAC',
    'HpaII': 'C/CGG',
    'HphI': 'GGTGANNNNNNNN/',
    'Hpy166II': 'GTN/NAC',
    'Hpy188I': 'TCN/GA',
    'Hpy188III': 'TC/NNGA',
    'Hpy99I': 'CGWCG/',
    'HpyAV': 'CCTTCNNNNNN/',
    'HpyCH4III': 'ACN/GT',
    'HpyCH4IV': 'A/CGT',
    'HpyCH4V': 'TG/CA',
    'I-CeuI': 'TAACTATAACGGTCCTAA/GGTAGCGAA',
    'I-SceI': 'TAGGGATAA/CAGGGTAAT',
    'ItaI': 'GC/NGC',
    'KasI': 'G/GCGCC',
    'KpnI': 'GGTAC/C',
    'KpnI-HF': 'GGTAC/C',
    'KspI': 'CCGC/GG',
    'LpnPI': 'CCDGNNNNNNNNNN/NNNN',
    'MaeI': 'C/TAG',
    'MaeII': 'A/CGT',
    'MaeIII': '/GTNAC',
    'MamI': 'GATNN/NNATC',
    'MboI': '/GATC',
    'MboII': 'GAAGANNNNNNNN/',
    'MfeI': 'C/AATTG',
    'MfeI-HF': 'C/AATTG',
    'MluCI': '/AATT',
    'MluI': 'A/CGCGT',
    'MluI-HF': 'A/CGCGT',
    'MluNI': 'TGG/CCA',
    'MlyI': 'GAGTCNNNNN/',
    'MmeI': 'TCCRACNNNNNNNNNNNNNNNNNNNN/',
    'MnlI': 'CCTCNNNNNNN/',
    'MroI': 'T/CCGGA',
    'MscI': 'TGG/CCA',
    'MseI': 'T/TAA',
    'MslI': 'CAYNN/NNRTG',
    'MspA1I': 'CMG/CKG',
    'MspI': 'C/CGG',
    'MspJI': 'CNNRNNNNNNNNN/NNNN',
    'MstI': 'TGC/GCA',
    'MstII': 'CC/TNAGG',
    'MunI': 'C/AATTG',
    'MvaI': 'CC/WGG',
    'MvnI': 'CG/CG',
    'MwoI': 'GCNNNNN/NNGC',
    'NaeI': 'GCC/GGC',
    'NarI': 'GG/CGCC',
    'NciI': 'CC/SGG',
    'NcoI': 'C/CATGG',
    'NcoI-HF': 'C/CATGG',
    'NdeI': 'CA/TATG',
    'NdeII': '/GATC',
    'NgoMI': 'G/CCGGC',
    'NgoMIV': 'G/CCGGC',
    'NheI': 'G/CTAGC',
    'NheI-HF': 'G/CTAGC',
    'NlaIII': 'CATG/',
    'NlaIV': 'GGN/NCC',
    'NmeAIII': 'GCCGAGNNNNNNNNNNNNNNNNNNNNN/',
    'NotI': 'GC/GGCCGC',
    'NotI-HF': 'GC/GGCCGC',
    'NruI': 'TCG/CGA',
    'NruI-HF': 'TCG/CGA',
    'NsiI': 'ATGCA/T',
    'NsiI-HF': 'ATGCA/T',
    'NspBII': 'CMG/CKG',
    'NspI': 'RCATG/Y',
    'NspII': 'GDGCH/C',
    'NspV': 'TT/CGAA',
    'PI-SceI': 'ATCTATGTCGGGTGC/GGAGAAAGAGGTAAT',
    'PacI': 'TTAAT/TAA',
    'PaeR7I': 'C/TCGAG',
    'PciI': 'A/CATGT',
    'PflFI': 'GACN/NNGTC',
    'PflMI': 'CCANNNN/NTGG',
    'PhoI': 'GG/CC',
    'PinAI': 'A/CCGGT',
    'PleI': 'GAGTCNNNN/N',
    'PluTI': 'GGCGC/C',
    'PmaCI': 'CAC/GTG',
    'PmeI': 'GTTT/AAAC',
    'PmlI': 'CAC/GTG',
    'PpuMI': 'RG/GWCCY',
    'PshAI': 'GACNN/NNGTC',
    'PsiI': 'TTA/TAA',
    'Psp1406I': 'AA/CGTT',
    'PspGI': '/CCWGG',
    'PspOMI': 'G/GGCCC',
    'PspXI': 'VC/TCGAGB',
    'PstI': 'CTGCA/G',
    'PstI-HF': 'CTGCA/G',
    'PvuI': 'CGAT/CG',
    'PvuI-HF': 'CGAT/CG',
    'PvuII': 'CAG/CTG',
    'PvuII-HF': 'CAG/CTG',
    'RcaI': 'T/CATGA',
    'RmaI': 'C/TAG',
    'RsaI': 'GT/AC',
    'RsrII': 'CG/GWCCG',
    'SacI': 'GAGCT/C',
    'SacI-HF': 'GAGCT/C',
    'SacII': 'CCGC/GG',
    'SalI': 'G/TCGAC',
    'SalI-HF': 'G/TCGAC',
    'SapI': 'GCTCTTCN/NNN',
    'Sau3AI': '/GATC',
    'Sau96I': 'G/GNCC',
    'SauI': 'CC/TNAGG',
    'SbfI': 'CCTGCA/GG',
    'SbfI-HF': 'CCTGCA/GG',
    'ScaI': 'AGT/ACT',
    'ScaI-HF': 'AGT/ACT',
    'ScrFI': 'CC/NGG',
    'SexAI': 'A/CCWGGT',
    'SfaNI': 'GCATCNNNNN/NNNN',
    'SfcI': 'C/TRYAG',
    'SfiI': 'GGCCNNNN/NGGCC',
    'SfoI': 'GGC/GCC',
    'SfuI': 'TT/CGAA',
    'SgrAI': 'CR/CCGGYG',
    'SmaI': 'CCC/GGG',
    'SmlI': 'C/TYRAG',
    'SnaBI': 'TAC/GTA',
    'SnoI': 'G/TGCAC',
    'SpeI': 'A/CTAGT',
    'SpeI-HF': 'A/CTAGT',
    'SphI': 'GCATG/C',
    'SphI-HF': 'GCATG/C',
    'SrfI': 'GCCC/GGGC',
    'Sse8387I': 'CCTGCA/GG',
    'SspBI': 'T/GTACA',
    'SspI': 'AAT/ATT',
    'SspI-HF': 'AAT/ATT',
    'SstI': 'GAGCT/C',
    'SstII': 'CCGC/GG',
    'StuI': 'AGG/CCT',
    'StyI': 'C/CWWGG',
    'StyI-HF': 'C/CWWGG',
    'StyD4I': '/CCNGG',
    'SwaI': 'ATTT/AAAT',
    'TaqI': 'T/CGA',
    'TfiI': 'G/AWTC',
    'ThaI': 'CG/CG',
    'TliI': 'C/TCGAG',
    'Tru9I': 'T/TAA',
    'TseI': 'G/CWGC',
    'Tsp45I': '/GTSAC',
    'Tsp509I': '/AATT',
    'TspMI': 'C/CCGGG',
    'TspRI': 'NNCASTGNN/',
    'Tth111I': 'GACN/NNGTC',
    'Van91I': 'CCANNNN/NTGG',
    'XbaI': 'T/CTAGA',
    'XcmI': 'CCANNNNN/NNNNTGG',
    'XhoI': 'C/TCGAG',
    'XhoII': 'R/GATCY',
    'XmaCI': 'C/CCGGG',
    'XmaI': 'C/CCGGG',
    'XmaIII': 'C/GGCCG',
    'XmnI': 'GAANN/NNTTC',
    'ZraI': 'GAC/GTC',
}


# Convert the cutting site to a compiles regex dictionary that can be used in _Sequence().digest(regex)
def _to_regex(input_dct):
    output_dct = {}
    mapper = str.maketrans({
        "A": "A",  # adenine
        "C": "C",  # cytosine
        "G": "G",  # guanine
        "T": "T",  # thymine
        "U": "U",  # uracil
        "N": ".",  # any
        "R": "[AG]",  # purine
        "Y": "[CT]",  # pyrimidine
        "K": "[GT]",  # keto
        "M": "[AC]",  # amino
        "S": "[CG]",  # strong
        "W": "[AT]",  # weak
        "B": "[CGT]",  # notA
        "D": "[AGT]",  # notC
        "H": "[ACT]",  # notG
        "V": "[ACG]",  # notT
    })
    for key in input_dct:
        if '/' not in input_dct[key]:
            raise ValueError('{} has not cutting site specified'.format(key))
        else:
            left, right = input_dct[key].split('/')
            output_dct[key] = r'((?:{1})?.*?{0}(?={1}))'.format(left.translate(mapper), right.translate(mapper))
    return output_dct

# Covert RESTRICTION_Enzymes dict into functional regex RESTRICTION_Enzymes dict
RESTRICTION_Enzymes = _to_regex(RESTRICTION_Enzymes)
