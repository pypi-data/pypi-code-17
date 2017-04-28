#!/usr/bin/env python


import sys
import os.path
import argparse


description = ("Merge multiple Metaphlan output tables, by filling with 0 "
               "in tables where a given taxon hasn't been found.\n"
               "Can remerge merged tables")
_sep='\t'


def _all_indices(V, elem):
    """ returns all indices of elem in list V"""
    start = 0
    indices = []
    while elem in V[start:]:
        start += V[start:].index(elem) + 1
        indices.append(start-1)
    return indices


def _line2tuple(line, iCol=0):
    """iCol is the column number of the ID names.
    returns: (ID, abundances)
    types:   (str, list)"""
    line = line.rstrip().split('\t')
    return line[iCol], line[:iCol] + line[iCol+1:]


def merge_tables(outputfile, samplefiles, idstr='ID', keep_original_IDs=True):
    """Each samplefile must be a list of size 1 or 2:
    samplefile = [filename, name] or just [filename]"""

    # add a default name when name is not specified (i.e len(f)==1)
    samplefiles = [f + [os.path.splitext(os.path.basename(f[0]))[0]]*(2-len(f)) \
                   for f in samplefiles]
    #remove identical files while keeping the order:
    samplefiles = [f for i,f in enumerate(samplefiles) if f not in samplefiles[:i]]
    files, names = zip(*samplefiles)
    
    # if same names for different file names (default names on files with same
    # basename), restore default name to full file name.
    for name in set(names):
        positions = _all_indices(names, name)
        if len(positions) > 1:
            for duplicated in positions:
                samplefiles[duplicated][1] = samplefiles[duplicated][0]

    # Build merged table of all samplefiles 
    samples = []
    taxa = set()
    for file_, samplename in samplefiles:
        with open(file_) as IN:
            table = dict(_line2tuple(line) for line in IN)
        
        if keep_original_IDs and table.get(idstr):
            table[idstr] = table.get(idstr)
        else:
            table[idstr] = [samplename]

        keys = set(table.keys())
        newtaxa    = keys - taxa
        oldtaxa    = taxa - keys
        
        for previous_table in samples:
            dim = len(previous_table[idstr])
            previous_table.update({ new: ["0"]*dim  for new in newtaxa})
        
        table.update({ old: ["0"]*len(table[idstr])  for old in oldtaxa})

        samples.append(table)
        taxa |= keys

    taxa.remove(idstr)
    
    OUT = sys.stdout if outputfile == "-" else open(outputfile, 'w')
    try:
        for taxon in [idstr] + sorted(taxa):
            OUT.write(taxon + \
                      _sep  + \
                      _sep.join(
                          _sep.join(sample[taxon]) for sample in samples) + \
                      "\n")
    finally:
        if outputfile == "-":
            OUT.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-o", "--outfile", default="-", help="default: stdout")
    parser.add_argument("input_table", nargs="+")
    parser.add_argument("--idstring", default="ID",
                        help=("row name of the ID line (sample name)."
                              "NOTE: it is '#SampleID' in metaphlan2 tables"))
    parser.add_argument("--trash-original-IDs", action='store_false',
                        dest="keep_original_IDs",
                        help="trash the ID names if present in input tables")

    args = parser.parse_args()
    
    merge_tables(args.outfile, [arg.split(",") for arg in args.input_table],
                 idstr=args.idstring, 
                 keep_original_IDs=args.keep_original_IDs)

