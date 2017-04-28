#!/usr/bin/env python

"""From a merged table of metaphlan abundances, creates the filtered data
divided by taxonomical levels"""


import re
import sys
import csv
import os.path

#taxlevels = ['k','p','c','o','f','g','s','t']
_intaxlevels='kpcofgst'

def dofilter(inputfile, outbase=None, filterout=1, keep_full_tax=False,
             taxlevels='kpcofgst', splitchar='|'):

    outbase = os.path.splitext(os.path.basename(inputfile))[0] if not outbase else outbase

    with open(inputfile) as IN:
        reader = csv.reader(IN, dialect='excel-tab')
        header = reader.next()
        n = len(header) - 1
        filtered_Data     = {tax_key: [header] for tax_key in _intaxlevels}
        filtered_samples  = {tax_key: [] for tax_key in _intaxlevels}
        filtered_taxa_nb  = {tax_key: [0] * n for tax_key in _intaxlevels}
        filtered_taxa_sum = {tax_key: [0] * n for tax_key in _intaxlevels}

        for tax_key, rowname, abundances in getassign_lines(reader, keep_full_tax,
                                                            splitchar=splitchar):

            row            = [0 if ab < filterout else ab for ab in abundances]
            low_abundances = [ab if ab < filterout else 0 for ab in abundances]
            islow_abundances = [low_ab > 0 for low_ab in low_abundances]

            filtered_taxa_nb[tax_key] = map(sum, zip(islow_abundances,
                                                     filtered_taxa_nb[tax_key]))
            filtered_taxa_sum[tax_key] = map(sum, zip(low_abundances,
                                                      filtered_taxa_sum[tax_key]))

            if not all(ab==0 for ab in row): 
                filtered_Data[tax_key].append([rowname] + row)
    
    for k, tax_key in enumerate(_intaxlevels):
        i = 1
        while i < len(filtered_Data[tax_key][0]) - 1:
            if all(row[i]==0 for row in filtered_Data[tax_key][1:]):
                sample = filtered_Data[tax_key][0][i]
                for child_tax in _intaxlevels[k:]:
                    filtered_samples[child_tax].append(sample)
                    filtered_Data[child_tax] = [row[:i]+row[i+1:] for row in \
                                                filtered_Data[child_tax]]
            else:
                i += 1

    for tax_key in taxlevels:
        with open(outbase + "_filtered_%s.tsv" % tax_key, 'w') as OUT:
            writer = csv.writer(OUT, dialect='excel-tab')
            writer.writerows(filtered_Data[tax_key])
    
    with open(outbase + "_filtered_samples.txt", 'w') as OUT:
        for tax_key in taxlevels:
            OUT.write(tax_key + ':\t' + '\t'.join(filtered_samples[tax_key]) + '\n')

    with open(outbase + "_filtered_taxa_nb.tsv", 'w') as OUT:
        writer = csv.writer(OUT, dialect='excel-tab')
        writer.writerow(header)
        for tax_key in taxlevels: 
            writer.writerow([tax_key] + filtered_taxa_nb[tax_key])

    with open(outbase + "_filtered_taxa_sum.tsv", 'w') as OUT:
        writer = csv.writer(OUT, dialect='excel-tab')
        writer.writerow(header)
        for tax_key in taxlevels:
            writer.writerow([tax_key] + filtered_taxa_sum[tax_key])
    

def getassign_lines(csvreader, keep_full_tax=False, intaxlevels=_intaxlevels,
                    splitchar='\|'):
    gettaxlevel = re.compile(r'([%s])__' % intaxlevels )
    for row in csvreader:
        fulltax = row.pop(0)
        gettax_key = gettaxlevel.findall(fulltax)
        if not gettax_key:
            tax_key = 'k'
            tax = fulltax
        else:
            tax_key = gettax_key[-1]
            gettax = re.compile(r'%s__([A-Za-z0-9_]+)(?:%s|$)' % (tax_key, splitchar))
            tax = fulltax if keep_full_tax else gettax.search(fulltax).group(1)
        yield tax_key, tax, [int(float(x)) if float(x)%1==0 else float(x) for x in row]


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile", help="merged metaphlan table")
    parser.add_argument("-o", "--outbase",
                        help=("base name of output files. default: "
                              "basename of input file"))
    parser.add_argument("-f", "--filterout", type=float, default=1,
                        help=("threshold for filtering out taxa: taxa under the "
                              "threshold in all samples will be trashed "
                              "[%(default)s %%]"))
    parser.add_argument("--keep-full-tax", action='store_true', default=False,
                        help=("Keep the original taxonomical assignment as row "
                            "name, not only the name at a given taxonomical level"))
    parser.add_argument("--splitchar", "-s", default="|",
                        help=("Character separating taxonomical levels in the "
                              "input row names [%(default)r]"))
    parser.add_argument('-t', '--taxlevels', default='kpcofgst',
                        help="taxonomical levels kept in the output [%(default)s]")
        
    args = parser.parse_args()
    dofilter(**vars(args))
