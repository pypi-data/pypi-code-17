#!/usr/bin/env python3
from collections import defaultdict
from sys import stderr
from os import path

import gffutils
import numpy as np
import pysam

import docopt


CLI = """
parephase -- Histogram coverage of 5' PARE data around stop sites

USAGE:
    parephase [options] -g GFF_FILE BAMFILE

OPTIONS:
    -P          Output counts per gene
    -u INT      Count INT bases upstream of the stop [default: 100]
    -d INT      Count INT bases downstream stream of the stop [default: 100]
    -g GFFFILE  GFF file describing gene models.
    -l GENIDS   File containing a list of gene models. If not given, all gene
                models are used, which can create inaccuate results. Please
                provide a list of representative gene models.
"""

# Copyright (c) 2016-2017 Kevin Murray <kdmfoss@gmail.com>

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def progprint(*args):
    print(*args, file=stderr, flush=True)


def load_gffdb(gfffile):
    '''Loads GFF from `gfffile`; returns DB cursor.'''

    if path.exists(gfffile + ".sqlite"):
        gfffile += ".sqlite"
    if gfffile.endswith(".sqlite"):
        progprint("Using cached annotation database")
        return gffutils.FeatureDB(gfffile)
    progprint("Loading annotation into database")
    db = gffutils.create_db(gfffile, gfffile + ".sqlite")
    progprint("\t... Finished!")
    return db


def calc_g2m(gffdb, transcript_id):
    """Returns 0-based position of the last nucleotide in the CDS of mRNA"""
    transcript = gffdb[transcript_id]
    exons = list(gffdb.children(transcript_id, featuretype='exon',
                                order_by='start'))
    mrna_pos = 0
    g2m = {}
    if transcript.strand == "+":
        mrna_pos = 0
        for exon in exons:
            for i in range(exon.start, exon.end + 1):
                g2m[i] = mrna_pos
                mrna_pos += 1
    else:
        for exon in reversed(exons):
            for i in range(exon.end, exon.start-1, -1):
                g2m[i] = mrna_pos
                mrna_pos += 1
    return g2m, {m: g for g, m in g2m.items()}


def find_stop_pos(gffdb, transcript_id):
    """Returns 0-based position of the last nucleotide in the CDS of mRNA"""
    transcript = gffdb[transcript_id]
    cdses = list(gffdb.children(transcript_id, featuretype='CDS',
                                order_by='start'))
    if transcript.strand == "+":
        three_prime = cdses[-1]
        stop_pos = three_prime.end   # Last position in CDS
    else:
        three_prime = cdses[0]
        stop_pos = three_prime.start  # Last pos in CDS, it's backwards
    return stop_pos


def make_roi_trees(gfffile, transcript_ids=None, upstream=100, downstream=50):
    gffdb = load_gffdb(gfffile)

    # ROIs are 1 tree for fwd & rev per chromosome
    roi_fs = defaultdict(dict)
    roi_rs = defaultdict(dict)

    # Default to all mRNA IDs
    if transcript_ids is None:
        mrnas = gffdb.all_features(featuretype='mRNA')
        transcript_ids = [m.id for m in mrnas]

    progprint("Loading transcripts from DB into ROI trees")
    i = 0
    for i, transcript_id in enumerate(sorted(transcript_ids)):
        if (i % 5000) == 0:
            progprint("\t...", i)

        transcript = gffdb[transcript_id]

        if transcript.featuretype != 'mRNA':
            continue

        chrom = transcript.chrom

        stop_pos = find_stop_pos(gffdb, transcript_id)
        tx_len = gffdb.children_bp(transcript_id)
        g2m, m2g = calc_g2m(gffdb, transcript_id)
        mstop = g2m[stop_pos]

        start = max(mstop - upstream, 0)
        end = min(start + upstream + downstream, tx_len)
        # wp = window pos, mp=mRNA pos, gp = genome pos. wp/mp 0-based, gp is 1
        for wp, mp in enumerate(range(start, end)):
            d = {
                "winpos": wp,
                "mrnapos": mp,
                "strand": transcript.strand,
                "tid": transcript.id
            }
            gp = m2g[mp]
            if transcript.strand == '+':
                roi_fs[chrom][gp] = d
            else:
                roi_rs[chrom][gp-1] = d
    progprint("\t... Finished, {:,} reads".format(i))
    return roi_fs, roi_rs


def processs_bam(bamfile, roi_trees, upstream=100, downstream=50):
    bam = pysam.AlignmentFile(bamfile, "rb")
    gcovs = defaultdict(lambda: np.zeros(upstream + downstream))
    fwdtree, revtree = roi_trees
    i = 0
    for i, read in enumerate(bam):
        if (i % 1000000) == 0:
            progprint("\t... {:0.0f}M reads".format(i / 1e6))

        # skip unmapped, weird or bad reads
        if read.is_unmapped or read.is_duplicate or read.is_paired or \
                read.is_secondary or read.is_supplementary:
            continue

        chrom = read.reference_name
        if read.is_reverse:
            roi_tree = revtree[chrom]
            pos = read.reference_end
        else:
            roi_tree = fwdtree[chrom]
            pos = read.reference_start

        try:
            feature = roi_tree[pos]
        except KeyError:
            # Not of any interest to us
            continue
        locus = feature["tid"]
        windowpos = feature["winpos"]

        gcovs[locus][windowpos] += 1
    progprint("\t... Finished, {:,} reads".format(i))
    bam.close()
    return gcovs


def calc_sum_all_transcripts(coverage):
    all = None
    for tx_vals in coverage.values():
        if all is None:
            all = np.zeros_like(tx_vals)
        all += tx_vals
    return all


def print_histogram(coverage, upstream, downstream, per_gene=False):
    all = calc_sum_all_transcripts(coverage)

    print("locus", *["pos_{}".format(i) for i in range(-upstream, downstream)],
          sep='\t')
    print("ALL", *list(all), sep='\t')

    if per_gene:
        for tx_id, coverage in sorted(coverage.items()):
            print(tx_id, *list(coverage), sep='\t')


def parse_txlist(txfile):
    with open(txfile) as fh:
        txlist = set()
        for line in fh:
            tx = line.rstrip()
            if tx:
                txlist.add(tx)
    return txlist


def main():
    from ._version import get_versions
    args = docopt.docopt(CLI, version=get_versions()["version"])

    gff = args['-g']
    if args['-l']:
        txlist = parse_txlist(args['-l'])
        progprint("Extracting", len(txlist), "transcripts")
    else:
        txlist = None
        progprint("Extracting all transcripts")
    upstream = int(args['-u'])
    downstream = int(args['-d'])

    progprint("Looking", upstream, "base upstream of TSS")
    progprint("Looking", downstream, "base downstream of TSS")

    progprint("Starting computation")

    progprint("Make ROI trees ...")
    roi_trees = make_roi_trees(gff, txlist, upstream, downstream)
    progprint("Make ROI trees ... done")

    progprint("Calculate 5'PARE histograms ...")
    coverage = processs_bam(args['BAMFILE'], roi_trees, upstream, downstream)
    progprint("Calculate 5'PARE histograms ... done")
    print_histogram(coverage, upstream, downstream, per_gene=args["-P"])

    progprint("Finished!")

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
