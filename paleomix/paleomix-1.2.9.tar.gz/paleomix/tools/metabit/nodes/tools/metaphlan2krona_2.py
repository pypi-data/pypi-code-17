#!/usr/bin/env python

# =====================================================================
_description = """
 Conversion script: from MetaPhlAn output to Krona text input file
 Author: Daniel Brami (daniel.brami@gmail.com)
 modified for metaBIT"""
# =====================================================================


import sys
import argparse
import re


def convert(inputfile, outputfile, no_underscore=False):

    re_candidates = re.compile(r"s__|unclassified\t")
    re_replace = re.compile(r"\w__")
    re_bar = re.compile(r"\|")

    IN  = open(inputfile,'r')  if inputfile  else sys.stdin
    OUT = open(outputfile,'w') if outputfile else sys.stdout

    try:
        for line in IN:
            if len(line.split("\t")) > 2:
                print >> sys.stderr, \
                      "Error: Wrong input file (more than two fields)"
                return 1

            if re.search(re_candidates, line):
                x=re.sub(re_replace, '\t', line)
                x=re.sub(re_bar, '', x)
                x=re.sub(r'_', ' ', x) if no_underscore else x

                x_cells = x.split('\t')
                lineage = '\t'.join(x_cells[:-1])
                abundance = x_cells[-1].rstrip('\n') 

                OUT.write(abundance + '\t' + lineage + '\n')
   
    finally:
        if OUT != sys.stdout:
            OUT.close()
        if IN != sys.stdin:
            IN.close()

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=_description,
                          formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('inputfile', type=str, nargs='?',
                        help='The input file is the MetaPhlAn standard result'
                             ' file. Default to stdin')
    parser.add_argument('outputfile', type=str, nargs='?',
                        help='the Krona output file name. Default to stdout' )
    parser.add_argument('--no-underscore', action='store_true',
                        help='convert underscores in fields to spaces')
    args = parser.parse_args()

    sys.exit(convert(args.inputfile, args.outputfile, args.no_underscore))

