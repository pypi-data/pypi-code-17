# (c) 2017, Florian P. Bayer <f.bayer@tum.de>
#
# sequence.py is part of the PyOmics project.
# It contains all kinds of Sequence objects that provide useful functionality.

# Import internal PyOmics modules
from PyOmics.constants import *

# Import standard library modules
import re
import warnings
import math
from collections import Counter


class _Sequence(object):
    """
    A Sequence is a data structure for biological strings and its associated information.
    
    The Sequence type is the core class in this module from which all other classes descend.
    A Sequence is simultaneously an immutable string-like object and an mutable information-storing dictionary that 
    holds additional and often important information about the sequence and makes the mere string much more meaningful, 
    without loosing track of what belongs together and what dose not. Changes upon the underlying sequence implies that 
    a new sequence object has to be generated since the underlying sequence is indivisibly connected to the existence
    of an Sequence object. This, however, is only true for the sequence. Information can be added, changed, and deleted
    without changing the overall meaning of the object.
    
    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string
    info : dict, optional
        additional information that describes the sequence in various ways
    
    Methods
    -------
    count()
        Analyze the composition of alphabet characters within the sequence
    find(motif)
        Find the occurrences of an string motif in the sequence
    digest(means)
        Digest the sequence into smaller sequence fragments by chosen means
        
    """
    alphabet = set(NUCLEOTIDE_Alphabet) | set(PROTEIN_Alphabet)

    def __init__(self, sequence, **information):
        """
        Initialization of an Sequence instance
        
        Parameters
        ----------
        sequence : str
            sequence is the biological sequence as string that gets stored as `seq` attribute
        information : **dict, optional
            information contains all other information that gets passed as keyword arguments. There is no limitation as
            to how many items can be passed.    
        """
        self.seq = sequence
        self.info = information
        self._counter = None

    def __repr__(self):
        """
        A string representation for a particular object
        
        Returns
        -------
        str
            entire sequence string that is the biological sequence of that object
        """
        return self.seq

    def __str__(self):
        """
        A formatted string representation for a particular object when used in a print statement
        
        Returns
        -------
        str
            sequence string that represents the biological sequence of that object
        
        Examples
        --------
        >>> print(_Sequence('ABC'))
        """
        if len(self.seq) >= 23:
            return self.seq[:10] + '...' + self.seq[-10:]
        return self.seq

    def __setitem__(self, key, value):
        """
        Dictionary-like setting of new additional information to the object
        
        Parameters
        ----------
        key : str
            The `key` to which the `value` is matched
        value : any
            The `value` can be anything one desires to store in connection with that instance
        
        Examples
        --------
        >>> _Sequence('ABC')['key'] = 'value'
        """
        self.info[key] = value

    def __delitem__(self, key):
        """
        Dictionary-like deleting of deprecated information from the object
        
        Parameters
        ----------
        key : str
            The `key` that shell be removed from the additional information
            
        Examples
        --------
        >>> del _Sequence('ABC')['key']
        """
        del self.info[key]

    def __missing__(self, key):
        """
        Called when user tries to access a piece of information that does not exist in the object
        
        Parameters
        ----------
        key : str
            The `key` that was mistakenly used to pull information
        """
        msg = 'You try to access information that does not exist! Check your key: {}'.format(key)
        warnings.warn(msg, UserWarning)
        return None

    def __getitem__(self, key):
        """
        Sequence slicing and dictionary-like access to sequence-associated information
        
        If `key` is a slice object or int, it will retrieve the specified sequence part according to the slice 
        operation. If `key` is a string object it will return sequence-associated information specified with the.
        
        Parameters
        ----------
        key : slice, int, str
            The `key` which shell be used to retrieve the desired information from the object

        Returns
        -------
        any, Sequence-like
            Anything that was stored to the `key` gets returned or a new Sequence according to the slice object
        
        Raises
        ------
        IndexError
            If slicing or integer is out of range for that underlying sequence
        TypeError
            If `key` is of a type other than slice, integer, string
        
        Examples
        --------
        >>> a_base = _Sequence('ABCD')[2]  # answer is 'C'
        >>> a_slice = _Sequence('ABCD')[1:3]  # answer is 'BC'
        >>> id_number = _Sequence('ABCD', id=123456789)['id']  # answer is 123456789
        """
        # Handle sequence slicing with python's slicing object. Return new String object
        if isinstance(key, slice) or isinstance(key, int):
            try:
                return self.__class__(self.seq[key])
            except IndexError:
                raise IndexError('sequence index out of range')

        #  Handle dict-like information access from self.info
        elif isinstance(key, str):
            if key in self.info:
                return self.info[key]
            else:
                return self.__missing__(key)

        else:
            raise TypeError("key must be of int, slice, or str")

    def __eq__(self, other):
        """
        Compare two objects of same kind with each other whether they are equal or not
        
        Sequence equality is based upon equality of the underlying sequence and the objects have to be of similar type.
        
        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an Sequence-like class to which the underlying sequence gets tested

        Returns
        -------
        bool
            True if equal or False if unequal
        
        Examples
        --------
        >>> _Sequence('ABC') == _Sequence('ABC')
        """
        if self.__class__ != other.__class__:
            return False
        return self.seq == other.seq

    def __ne__(self, other):
        """
         Compare two objects of same kind with each other whether they are unequal or not
         
        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an Sequence-like class to which the underlying sequence gets tested

        Returns
        -------
        bool
            True if unequal or False if equal
        
        Examples
        --------
        >>> _Sequence('ABC') != _Sequence('DEF')
        """
        if self.__class__ != other.__class__:
            return True
        return self.seq != other.seq

    def __add__(self, other):
        """
        Concatenation of two similar Sequence-like objects 
        
        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an similar Sequence-like class 

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the concatenated sequence. No information gets transferred whatsoever
        
        Raises
        ------
        TypeError
            If `other` is not an instance of the same type as self

        Examples
        --------
        >>> new = _Sequence('ABC') + _Sequence('DEF')
        """
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} + {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __radd__(self, other):
        """
        Concatenation of two similar Sequence-like objects 

        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an similar Sequence-like class 

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the concatenated sequence. No information gets transferred whatsoever
        
        Raises
        ------
        TypeError
            If `other` is not an instance of the same type as self

        Examples
        --------
        >>> new = _Sequence('ABC') + _Sequence('DEF')
        """
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} + {}".format(other.__class__.__name__, self.__class__.__name__, )
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __iadd__(self, other):
        """
        Concatenation of two similar Sequence-like objects 

        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an similar Sequence-like class 

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the concatenated sequence. No information gets transferred whatsoever
        
        Raises
        ------
        TypeError
            If `other` is not an instance of the same type as self

        Examples
        --------
        >>> var = _Sequence('ABC')
        >>> var += _Sequence('DEF')
        """
        if self.__class__ != other.__class__:
            error_message = "Sequence concatenation is only possible if both sequences are of similar type. " \
                            "Found: {} =+ {}".format(self.__class__.__name__, other.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(self.seq + other.seq)

    def __mul__(self, n):
        """
        Repeating a Sequence multiple times
        
        Parameters
        ----------
        n : int
            The number 'n' times the sequence shell be repeated

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the `n` times repeated sequence. No information gets transferred whatsoever.
        
        Raises
        ------
        TypeError
            If `n` is not an integer

        Examples
        --------
        >>> new = _Sequence('ABC') * 4
        """
        if not isinstance(n, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} * {}".format(self.__class__.__name__, n.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(n * self.seq)

    def __rmul__(self, n):
        """
        Repeating a Sequence multiple times

        Parameters
        ----------
        n : int
            The number 'n' times the sequence shell be repeated

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the `n` times repeated sequence. No information gets transferred whatsoever.
        
        Raises
        ------
        TypeError
            If `n`is not an integer
        
        Examples
        --------
        >>> new = 4 * _Sequence('ABC')
        """
        if not isinstance(n, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} * {}".format(n.__class__.__name__, self.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(n * self.seq)

    def __imul__(self, n):
        """
        Repeating a Sequence multiple times

        Parameters
        ----------
        n : int
            The number 'n' times the sequence shell be repeated

        Returns
        -------
        Sequence-like object
            A new Sequence-like object with the `n` times repeated sequence. No information gets transferred whatsoever.
        
        Raises
        ------
        TypeError
            If `n`is not an integer

        Examples
        --------
        >>> var = _Sequence('ABC')
        >>> var *= 4
        """
        if not isinstance(n, int):
            error_message = "Sequence repetition is only possible with an integer. " \
                            "Found: {} =* {}".format(self.__class__.__name__, n.__class__.__name__)
            raise TypeError(error_message)
        return self.__class__(n * self.seq)

    def __len__(self):
        """
        Length determination of the sequence
        
        Returns
        -------
        int
            number of characters in the sequence (length)
        
        Examples
        --------
        >>> len(_Sequence('ABC'))
        """
        return len(self.seq)

    def __contains__(self, other):
        """
        Pythonic way to check whether a Sequence-like object is a substring of an other Sequence-like object 
        
        Parameters
        ----------
        other : Sequence-like
            An `other` instance of an similar Sequence-like class 

        Returns
        -------
        bool
            True if `other` is indeed in the sequence; else False
        
        Raises
        ------
        TypeError
            If `other` is not an instance of the same type as self
        
        Examples
        --------
        >>> _Sequence('A') in _Sequence('ABC')
        """
        if self.__class__ != other.__class__:
            error_message = "Subsequence search is only possible if both sequences are of similar type. " \
                            "Found: {} in {}".format(other.__class__.__name__, self.__class__.__name__)
            raise TypeError(error_message)
        return other.seq in self.seq

    def __iter__(self):
        """
        Efficient iteration over characters of the underlying sequence
        
        Yields
        ------
        str
            A single character of the sequence
        
        Examples
        --------
        >>> for char in _Sequence('ABC'): print(char)
        """
        for char in self.seq:
            yield char

    def count(self):
        """
        Analysis of the composition of alphabet characters within the sequence
        
        Returns
        -------
        Counter
            A Counter object storing the composition
            
        Examples
        --------
        >>> c = _Sequence('ABC').count()
        """
        if not self._counter:
            self._counter = Counter(self.seq)
        return self._counter

    def find(self, motif, overlap=True, start=0):
        """
        Find the occurrences of an string motif in the sequence
        
        Parameters
        ----------
        motif : str
            A motif that is searched against the sequence
        overlap : bool, optional
            A flag parameter to specify whether to include overlaps or not (default is True)
        start : int, optional
            A starting index other then the beginning of the sequence (default is 0)
        Returns
        -------
        list
            A list of integers referencing the starting indexes of each motif occurrence in the sequence
        
        Examples
        --------
        >>> lst = _Sequence('ABCD').find('CD')
        """
        # use an iterator for each next str.find index (efficient!!)
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

    def digest(self, means, sort=True, as_str=False):
        """
        Sequence digestion into smaller sequence fragments
        
        Parameters
        ----------
        means : pattern
            The 'means' by which the sequence gets fragmented is a regex pattern to define cutting sites in the sequence
        sort : bool, optional
            A flag parameter to specify whether the retruned list shell be sorted or not (default is True)
        as_str : bool, optional
            A flag parameter to specify the type of the fragment Sequence as string (default is False -> Sequence-like) 
        Returns
        -------
        list
            a list of sequence fragments either as string or sequence-like object 
        
        Examples
        --------
        >>> fragments = _Sequence('ABCDE').digest(r'[C]')
        """
        # a sorted list of all unique fragment strings
        fragments = list({*re.split(means, self.seq)})

        # if sorted is True: sort the fragments by length in reversed order
        if sort:
            fragments = sorted(fragments, key=len, reverse=True)

        # if as string is True: return the fragments simply as strings; else: as *Sequence objects
        if as_str:
            return fragments
        return [self.__class__(f) for f in fragments]


class _NucleotideSequence(_Sequence):
    """
    A Nucleotide Sequence is a data structure for DNA and RNA sequences and its associated information.
    
    The Nucleotide Sequence is the parent class for DNA and RNA Sequences as well as is a descendant of Sequence.
    This means that a Nucleotide Sequence summarizes methods common to both DNA and RNA. It also behaves as one would 
    expect from a regular Sequence type.
    
    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string
    info : dict, optional
        additional information that describes the sequence in various ways
    
    Methods
    -------
    atgc()
        Analysis of the guanine and cytosine extent (GC) of the nucleotide sequence
    count()
        Analyze the composition of alphabet characters within the nucleotide sequence
    find(motif)
        Find the occurrences of an string motif in the nucleotide sequence
    digest(means)
        Digest the nucleotide sequence into smaller nucleotide sequence fragments by chosen means
    gc()
        Analyze the guanine and cytosine content (GC) of the nucleotide sequence
    reverse()
        Reverse the nucleotide sequence
    complement(base_pairing)
        Complement the nucleotide sequence based on base pairing mapper
    reverse_complement(base_pairing)
        Reverse and Complement the nucleotide sequence based on base pairing 
    translate(codon)
        Translate nucleotide Sequence into a protein Sequence
    """
    alphabet = NUCLEOTIDE_Alphabet

    def gc(self):
        """
        Analysis of the guanine and cytosine content (GC) of the nucleotide sequence
        
        Returns
        -------
        float
            the ratio of guanine and cytosine in the nucleotide sequence
        
        References
        ----------
        https://en.wikipedia.org/wiki/GC-content
        
        Examples
        --------
        >>> gc = _NucleotideSequence('ACGT').gc()
        """
        return (self.seq.count('C') + self.seq.count('G')) / len(self.seq)

    def atgc(self):
        """
        Analysis of the guanine and cytosine extent (GC) of the nucleotide sequence

        Returns
        -------
        float
            the ratio of guanine and cytosine relative to adenine and thymine

        References
        ----------
        https://en.wikipedia.org/wiki/GC-content

        Examples
        --------
        >>> gc = _NucleotideSequence('ACGT').atgc()
        """
        # TODO: Maybe use a Counter to handle more ambiguous characters
        # TODO: Think about possibilities to include ambiguous bases. Maybe as flag? including them or not T/F?
        return ((self.seq.count('A') + self.seq.count('T') + self.seq.count('U')) /
                (self.seq.count('C') + self.seq.count('G')))

    def reverse(self):
        """
        Building of the reverse nucleotide sequence from the nucleotide sequence
        
        Returns
        -------
        Sequence-like
            The reversed nucleotide sequence as a new object, but information is copied to the new object
        
        Examples
        --------
        >>> rev = _NucleotideSequence('ACGT').reverse()
        """
        return self.__class__(self.seq[::-1], **self.info)

    def complement(self, base_pairing):
        """
        Building of the complement nucleotide sequence from the nucleotide sequence
        
        Parameters
        ----------
        base_pairing : dict
            A mapping that maps one base to its corresponding base
            
        Returns
        -------
        Sequence-like
            The complement nucleotide sequence as a new object, but information is copied to the new object
        
        Examples
        --------
        >>> dna = _NucleotideSequence('ACGT').complement(DNA_Base_Pairing)
        >>> rna = _NucleotideSequence('ACGU').complement(RNA_Base_Pairing)
        """
        table = str.maketrans(base_pairing)
        return self.__class__(self.seq.translate(table), **self.info)

    def reverse_complement(self, base_pairing):
        """
        Building of the reverse complement of the nucleotide sequence
        
        Parameters
        ----------
        base_pairing : dict
            A mapping that maps one base to its corresponding base

        Returns
        -------
        Sequence-like
            The reverse-complement nucleotide sequence as a new object, but information is copied to the new object
            
        Examples
        --------
        >>> dna = _NucleotideSequence('ACGT').reverse_complement(DNA_Base_Pairing)
        >>> rna = _NucleotideSequence('ACGU').reverse_complement(RNA_Base_Pairing)
        """
        table = str.maketrans(base_pairing)
        return self.__class__(self.seq.translate(table)[::-1], **self.info)

    def translate(self, codon, from_start=False):
        """
        Translation of the nucleotide sequence into a protein Sequence 
        
        Parameters
        ----------
        codon : dict
            A mapping that maps a nucleotide tripplet to its corresponding amino acid
        from_start : bool, optional
            A flag parameter to specify whether translation shell start at index 0 or at the start codon Methionine 
            (default is False which means that translation starts at the start codon) 
            
        Returns
        -------
        ProteinSequence
            A new protein sequence object that got all information passed, though
        
        Examples
        --------
        >>> prot1 = _NucleotideSequence('ATGC').translate(DNA_Codons)
        >>> prot2 = _NucleotideSequence('AUGC').translate(RNA_Codons)
        """
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
        return ProteinSequence(protein_seq, **self.info)


class ProteinSequence(_Sequence):
    """
    A Protein Sequence is a data structure for protein sequences and its associated information.
    
    The Protein Sequence class is a descendant of Sequence.
    This means that a Protein Sequence behaves as one would expect from a regular Sequence type.
    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string
    info : dict, optional
        additional information that describes the sequence in various ways
    
    Methods
    -------
    count()
        Analyze the composition of alphabet characters within the sequence
    find(motif)
        Find the occurrences of an string motif in the sequence
    digest(means)
        Digest the sequence into smaller sequence fragments by chosen means
    mass()
        Calculate the monoisotopic mass of the entire protein Sequence
        
    """
    alphabet = PROTEIN_Alphabet

    def mass(self, ndigits=5):
        """
        Calculation of the monoisotopic mass of the entire protein Sequence
        
        Parameters
        ----------
        ndigits : int, optional
            the number of digits to round the mass float (default is 5 digits)

        Returns
        -------
        float
            the total monoisotopic mass of the protein sequence
        
        Examples
        --------
        >>> weight = ProteinSequence('PEPTIDE').mass()
        """
        # The weight of an empty sequence is 0 Dalton
        if len(self) == 0:
            return 0

        # else analyze the Sequence:
        # If counter is available: fetch it
        if self._counter:
            counter = self._counter
        # else calculate it and store it for later use
        else:
            counter = Counter(self.seq)
            self._counter = counter

        # Refuse to calculate the weight when B or Z is present in the sequence
        if 'B' in counter or 'Z' in counter:
            msg = 'You sequence <{}> contains "B" ans/or "Z" chars. ' \
                  'It is not possible to calculate the mass from those.'.format(str(self))
            warnings.warn(msg, UserWarning)
            return None

        # Calculate the mass
        h2o = 18.010565  # Monoisotopic mass of terminal water in Dalton
        totalmass = sum([AMINOACIDS_Mono_Mass[aminoacid] * n for aminoacid, n in counter.items()]) + h2o
        return round(totalmass, ndigits)

    def pI(self, ref='Wikipedia', delta=10 ** -4, ndigits=2):
        """
        Calculate the theoretical isoelectric point for the protein sequence
        
        Calculate the pI is the pH value where the net charge of the sequence is 0. This pH value is found through a 
        bisect search algorithm. The net charge function calculates the protonation state according to the Henderson-
        Hasselbalch equation [1] for a moiety that can protonate and deprotonate. The assumption here is that each 
        moiety acts independently from each other in an acid-base reaction, so that the molecule's net charge is the 
        mere sum of all acid-base moieties, which are the N-terminus:(RNH2), C-terminus:(RCOOH), C:(RSH), D:(RCOOH), 
        E:(RCOOH), H:(R2NH), K(RNH2), R(Guanidinyl), Y(ROH).
        
        Parameters
        ----------
        ref : str, optional
            name of the reference that will be used to provide pka values for the acid-base reaction
        delta: float, optional
            the cutoff value `delta` specifies who close the net charge is allowed to differ from 0
        ndigits: int
            the number of digits that will be returned 
        
        Returns
        -------
        float
            the pI value for the given protein sequence
        
        References
        ----------
        [1] https://en.wikipedia.org/wiki/Henderson–Hasselbalch_equation
        
        Examples
        --------
        >>> pI = ProteinSequence('DEGK').pI()
        """
        def charge_state(ph, pkas, n):
            """
            the charge of the protein is equivalent to the sum of the fractional charges of the protein’s charged groups
            """

            def alpha(pka_value, ph_value):
                """
                determine the degree of dissociation (=alpha value) according to the Henderson-Hasselbalch equation
                """
                return 1 / (1 + pow(10, (pka_value - ph_value)))

            # For ionizable groups that are able to deprotonate to a charge of -1 (e.g., OH & COOH),
            # multiply the calculated dissociation constant by -1.
            # For ionizable groups that are able to deprotonate to a charge of 0 (e.g, NH3+), take the complement of the
            # dissociation constant(1-alpha) and multiply the constant by +1.
            # The net charge of the amino acid will be the sum of the charges of all of the ionizable groups.
            return sum([+ (1 - alpha(pkas['NH2'], ph)),
                        - alpha(pkas['COOH'], ph),
                        - alpha(pkas['C'], ph) * n['C'],
                        - alpha(pkas['D'], ph) * n['D'],
                        - alpha(pkas['E'], ph) * n['E'],
                        + (1 - alpha(pkas['H'], ph)) * n['H'],
                        + (1 - alpha(pkas['K'], ph)) * n['K'],
                        + (1 - alpha(pkas['R'], ph)) * n['R'],
                        - alpha(pkas['Y'], ph) * n['Y'],
                        ])

        # Analyze the Sequence:
        # If available: fetch it
        if self._counter:
            counter = self._counter
        # else calculate it and store it for later use
        else:
            counter = Counter(self.seq)
            self._counter = counter

        # define pH boundaries and set initial charge state at pH = 7.0
        low, mid, high = 0.0, 7.0, 14.0
        z = charge_state(mid, AMINOACIDS_Pkas[ref], counter)

        # perform the bisect search until: z in (0 ± delta)
        while abs(z) >= delta:
            # positive charge means that mid pH is too low
            if z > 0:
                low, mid = mid, (mid + high) / 2
            # negative charge means that mid pH is too high
            else:
                high, mid = mid, (mid + low) / 2
            # calculate the new charge based on the new middle pH
            z = charge_state(mid, AMINOACIDS_Pkas[ref], counter)
        return round(mid, ndigits)


class DNASequence(_NucleotideSequence):
    """
    A DNA Sequence is a data structure for DNA sequences and its associated information.
    
    The DNA Sequence class is a descendant of Sequence and more specific of Nucleotide Sequence.
    This means that a DNA Sequence behaves as one would expect from a regular Nucleotide Sequence type.
    
    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string
    info : dict, optional
        additional information that describes the sequence in various ways
    
    Methods
    -------
    count()
        Analyze the composition of alphabet characters within the DNA sequence
    find(motif)
        Find the occurrences of an string motif in the DNA sequence
    digest(means)
        Digest the DNA sequence into smaller nucleotide sequence fragments by chosen means
    gc()
        Analyze the guanine and cytosine content (GC) of the DNA sequence
    reverse()
        Reverse the DNA sequence
    complement()
        Complement the DNA sequence based on base pairing mapper
    reverse_complement()
        Reverse and Complement the DNA sequence based on base pairing 
    translate()
        Translate DNA Sequence into a protein Sequence
    """
    def complement(self, **kwargs):
        return super(DNASequence, self).complement(DNA_Base_Pairing)

    def reverse_complement(self, **kwargs):
        return super(DNASequence, self).reverse_complement(DNA_Base_Pairing)

    def translate(self, **kwargs):
        return super(DNASequence, self).translate(DNA_Codons, **kwargs)

    def transcribe(self):
        return RNASequence(self.seq.replace("T", "U"), **self.info)


class RNASequence(_NucleotideSequence):
    """
    A RNA Sequence is a data structure for RNA sequences and its associated information.

    The RNA Sequence class is a descendant of Sequence and more specific of Nucleotide Sequence.
    This means that a RNA Sequence behaves as one would expect from a regular Nucleotide Sequence type.

    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string
    info : dict, optional
        additional information that describes the sequence in various ways

    Methods
    -------
    count()
        Analyze the composition of alphabet characters within the RNA sequence
    find(motif)
        Find the occurrences of an string motif in the RNA sequence
    digest(means)
        Digest the RNA sequence into smaller nucleotide sequence fragments by chosen means
    gc()
        Analyze the guanine and cytosine content (GC) of the RNA sequence
    reverse()
        Reverse the RNA sequence
    complement()
        Complement the RNA sequence based on base pairing mapper
    reverse_complement()
        Reverse and Complement the RNA sequence based on base pairing 
    translate()
        Translate RNA Sequence into a protein Sequence
    """
    def complement(self, **kwargs):
        return super(RNASequence, self).complement(RNA_Base_Pairing)

    def reverse_complement(self, **kwargs):
        return super(RNASequence, self).reverse_complement(RNA_Base_Pairing)

    def translate(self, **kwargs):
        return super(RNASequence, self).translate(RNA_Codons, **kwargs)

    def reverse_transcribe(self):
        return DNASequence(self.seq.replace("U", "T"), **self.info)


class Primer(DNASequence):
    """
    A Primer is a short oligonucleotid DNA Sequence data structure for Primers and its associated information.

    The Primer class is a descendant of DNA Sequence.
    This means that a Primer Sequence behaves as one would expect from a regular DNA Sequence type.

    Attributes
    ----------
    seq : str
        sequence represents the biological sequence as string. Not allowed to be longer than 50nts
    info : dict, optional
        additional information that describes the sequence in various ways

    Methods
    -------
    count()
        Analyze the composition of alphabet characters within the DNA sequence
    find(motif)
        Find the occurrences of an string motif in the DNA sequence
    digest(means)
        Digest the Primer sequence into smaller nucleotide sequence fragments by chosen means
    gc()
        Analyze the guanine and cytosine content (GC) of the DNA sequence
    reverse()
        Reverse the Primer sequence
    complement()
        Complement the Primer sequence based on base pairing mapper
    reverse_complement()
        Reverse and Complement the Primer sequence based on base pairing 
    translate()
        Translate Primer Sequence into a protein Sequence
    melting_temp()
        Calculate the theoretical melting temperature
    """
    def __init__(self, sequence, **information):
        """
        Initialization of Primer instance

        Parameters
        ----------
        sequence : str
            sequence is the biological sequence as string that gets stored as `seq` attribute. 
            Not allowed to be longer than 50nts
        information : **dict, optional
            information contains all other information that gets passed as keyword arguments. There is no limitation as
            to how many items can be passed.  
            
        Raises
        ------
        ValueError
            If sequence is longer that 50nt
        """
        if len(sequence) > 50:
            raise ValueError('Sequence length is not allowed to be longer than 50nt. Use DNA Sequence class instead.')
        super(DNASequence, self).__init__(sequence, **information)

    def melting_temp(self, concentration=200,  sodium=50, method='nearest-neighbor'):
        """
        Calculate the theoretical melting temperature
        
        The theoretical melting temperature TM in C° is the temperature at which half of the strands are in the 
        double-helical state and half are in the “random-coil” state. There exists several methods to calculate the TM 
        that all use different strategies to calculate the TM. Depending on the sequence, the values obtained from 
        different methods can drastically. Pleas make sure that you know why you use which method. The thermodynamical 
        nearest-neighbor approach is the most-widely accepted method to use.
        
        Parameters
        ----------
        concentration : float, optional
            Primer concentration in nmol, (default is 200 nM)
        sodium : float, optional
            Na+ concentration in mMol, (default is 50 mM)
        method : str, optional
            Choose one of the following methods to calculate the TM:
            ['marmur', 'wallace', 'salt-adjusted', 'nearest-neighbor'], (default is 'nearest-neighbor')
        
        Returns
        -------
        float
            The theoretical melting temperature TM in C°
    
        Raises
        ------
        ValueError
            If method is not one of the specified methods
        
        Notes
        -----
        The melting temperature is defined as the temperature at which half of the strands are in the double-helical 
        state and half are in the “random-coil” state. It is an important parameter in Polymerase chain reactions (PCR).
        It is critical to determine a proper temperature for the annealing step because efficiency and specificity are 
        strongly affected by the annealing temperature. This temperature must be low enough to allow for hybridization 
        of the primer to the strand, but high enough for the hybridization to be specific, i.e., the primer should bind 
        only to a perfectly complementary part of the strand, and nowhere else. If the temperature is too low, the 
        primer may bind imperfectly. If it is too high, the primer may not bind at all. A typical annealing temperature 
        is about 3–5 °C below the Tm of the primers used.
        
        References
        ----------
        [1] https://en.wikipedia.org/wiki/Polymerase_chain_reaction
        [2] Marmur J and Doty P (1962) J Mol Biol 5:109-118
        [3] Wallace RB et al. (1979) Nucleic Acids Res 6:3543-3557, PMID 158748
        [4] Schildkraut et al. 1965, PMID 5889540 salt correction formulae
        [5] SantaLucia 1998, PMID 9465037 thermodynamics & salt correction
        
        Examples
        --------
        >>> tm = Primer('CATGCCATGGAAAAACGGGCGATTTATCC').melting_temp()
        """
        # If counter is available: fetch it
        if self._counter:
            n = self._counter
        # else calculate it and store it for later use
        else:
            n = Counter(self.seq)
            self._counter = n

        # constants:
        gas_constant = 1.987  # gas constant in cal/(K*mol)
        salt_correction_factor = 0.114  # kcal/(K*mol) at T=310K
        concentration *= 10 ** -9  # transfer from nmol to mol
        sodium *= 10 ** -3  # transfer from mmol to mol
        # ΔH° in cal/mol from http://www.pnas.org/content/95/4/1460/T2.expansion.html
        formation_enthalpy = {'AA': -7900, 'AT': -7200, 'AG': -7800, 'AC': -8400,
                              'TA': -7200, 'TT': -7900, 'TG': -8500, 'TC': -8200,
                              'GA': -8200, 'GT': -8400, 'GG': -8000, 'GC': -9800,
                              'CA': -8500, 'CT': -7800, 'CC': -8000, 'CG': -10600,
                              }
        initial_enthalpy = {'A': 2300, 'T': 2300, 'G': 100, 'C': 100}
        # ΔS° cal/k·mol from http://www.pnas.org/content/95/4/1460/T2.expansion.html
        formation_entropy = {'AA': -22.2, 'AT': -20.4, 'AG': -21.0, 'AC': -22.4,
                             'TA': -21.3, 'TT': -22.2, 'TG': -22.7, 'TC': -22.2,
                             'GA': -22.2, 'GT': -22.4, 'GG': -19.9, 'GC': -24.4,
                             'CA': -22.7, 'CT': -21.0, 'CC': -19.9, 'CG': -27.2,
                             }
        initial_entropy = {'A': 4.1, 'T': 4.1, 'G': -2.8, 'C': -2.8}

        # calculate according to Marmur
        # not recommended for more than 13nt; assumes 50mM monovalent cations
        if method == 'marmur':
            if len(self.seq) > 13:
                warnings.warn('not recommended for more than 13nt', UserWarning)
            elif sodium != 50*10**-3:
                warnings.warn('assumes 50mM monovalent cations', UserWarning)
            t = 2 * (n['A'] + n['T']) + 4 * (n['G'] + n['C'])

        # calculate according to Wallace
        elif method == 'wallace':
            t = 64.9 + 41 * (n['G'] + n['C'] - 16.4) / (n['G'] + n['C'] + n['A'] + n['T'])

        # calculate according to the salt adjusted method
        elif method == 'salt-adjusted':
            total = n['G'] + n['C'] + n['A'] + n['T']
            t = 100.5 + (41 * (n['G'] + n['C']) / total) - (820 / total) + (16.6 * math.log10(sodium))

        # calculate according to the thermodynamical nearest neighbor model
        elif method == 'nearest-neighbor':
            # calculate the initial enthalpy and entropy
            enthalpy = initial_enthalpy[self.seq[0]] + initial_enthalpy[self.seq[-1]]
            entropy = initial_entropy[self.seq[0]] + initial_entropy[self.seq[-1]]

            # add the salt enthalpy factor
            entropy += salt_correction_factor / 310 * 1000 * math.log(sodium, math.e) * len(self.seq)

            for i in range(len(self.seq) - 1):
                enthalpy += formation_enthalpy[self.seq[i:i + 2]]
                entropy += formation_entropy[self.seq[i:i + 2]]

            t = enthalpy / (entropy + gas_constant * math.log(concentration / 4, math.e)) - 273.15

        else:
            raise ValueError('method <{}> is not implemented. Use help to see available methods'.format(method))

        return round(t, 2)


if __name__ == '__main__':
    pass
