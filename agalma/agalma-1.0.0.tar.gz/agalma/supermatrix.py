#!/usr/bin/env python
#
# Agalma - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2017 Brown University. All rights reserved.
#
# This file is part of Agalma.
#
# Agalma is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agalma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agalma.  If not, see <http://www.gnu.org/licenses/>.

"""
Concatenates alignments of orhologous sequences to create a supermatrix.
It also creates a supermatrix with a given proportion of gene occupancy.
"""

import numpy as np
import os
import shutil
from Bio import SeqIO
from itertools import izip
from StringIO import StringIO

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline("supermatrix", __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the alignments from a previous run of multalign.""")

pipe.add_arg("--proportion", type=float, default=None, help="""
	If specified, creates a supermatrix with gene occupancy equal to
	proportion in [0-1].""")

### STAGES ###

@pipe.stage
def init(id, previous):
	"""Find alignments in database"""

	try:
		prev_id = diagnostics.lookup_prev_run(id, previous, "multalign").id
	except AttributeError:
		utils.die("no previous multalign runs found for id", id)
	diagnostics.log("prev_id", prev_id)

	seq_type = diagnostics.lookup(prev_id, diagnostics.INIT)["seq_type"]
	diagnostics.log_exit("seq_type", seq_type)

	taxa = {}
	gene_seqs = {}
	gene_lengths = {}

	for id, alignment in database.select_alignments(prev_id):
		# Build a dictionary of taxa/sequences in this cluster
		seqs = {}
		for record in SeqIO.parse(StringIO(alignment), "fasta"):
			seqs[record.id.partition('@')[0]] = str(record.seq)
		gene_lengths[id] = max(map(len, seqs.itervalues()))
		for taxon in seqs:
			# All sequences in the multiple alignment should have the same length
			assert len(seqs[taxon]) == gene_lengths[id]
			taxa[taxon] = taxa.get(taxon, 0) + 1
		gene_seqs[id] = seqs

	ingest("prev_id", "seq_type", "taxa", "gene_seqs", "gene_lengths")


@pipe.stage
def supermatrix(taxa, gene_seqs, gene_lengths):
	"""Concatenate multiple alignments into a supermatrix"""
	
	# Sort from best to worst sampled genes.
	genes = sorted(gene_seqs, key=gene_seqs.get, reverse=True)

	# Sort from best to worst sampled taxa.
	taxa = sorted(taxa, key=taxa.get, reverse=True)

	superseq = dict([(taxon, []) for taxon in taxa])
	occupancy = np.zeros((len(genes), len(taxa)), dtype=np.uint32)

	for i, gene in enumerate(genes):
		for j, taxon in enumerate(taxa):
			# Select the sequence for the taxon if it was in the alignment for this
			# gene, otherwise use a sequence of all gaps
			seq = gene_seqs[gene].get(taxon, '-' * gene_lengths[gene])
			superseq[taxon].append(seq)
			occupancy[i,j] = sum(1 for c in seq if c != '-')

	ingest("genes", "taxa", "superseq", "occupancy")


@pipe.stage
def trim(genes, taxa, occupancy, proportion):
	"""Trim the supermatrix to the specified proportion of occupancy"""

	cum_occupancy = np.cumsum(np.sum(occupancy.astype(bool), axis=1), dtype=np.float64)
	cum_occupancy /= np.cumsum(len(taxa) * np.ones(len(genes)))

	ngenes = len(genes)
	if proportion:
		for i, val in enumerate(cum_occupancy):
			if val < proportion:
				ngenes = i
				break
		if ngenes <= 0:
			utils.die("supermatrix is empty")
		utils.info("keeping", ngenes, "out of", len(genes), "genes")
	else:
		utils.info("no proportion specified... skipping")

	ingest("ngenes")


@pipe.stage
def parse(_run_id, genes, taxa, gene_lengths, superseq, occupancy, ngenes):
	"""Store the supermatrix in the database"""

	# flatten sequences
	for taxon in taxa:
		superseq[taxon] = ''.join(superseq[taxon][:ngenes])

	database.store(_run_id, "taxa", taxa)
	database.store(_run_id, "genes", genes[:ngenes])
	database.store(_run_id, "superseq", superseq)
	database.store(_run_id, "gene_lengths", map(gene_lengths.get, genes[:ngenes]))
	database.store(_run_id, "occupancy", occupancy[:ngenes,:])


### RUN ###

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

### REPORT ###

class Report(report.BaseReport):
	def init(self):
		self.name = pipe.name
		self.basename = "%d.supermatrix" % self.run_id
		# Lookups
		self.lookup_attribute(diagnostics.INIT, "proportion")
		self.lookup_attribute(diagnostics.EXIT, "seq_type")
		self.retrieve("taxa")
		self.retrieve("genes")
		self.retrieve("superseq")
		self.retrieve("gene_lengths")
		self.retrieve("occupancy")
		# Generators
		self.generator(self.write_files)
		self.generator(self.occupancy_table)
		self.generator(self.occupancy_plot)
		self.generator(self.cum_occupancy_plot)
		self.generator(self.taxon_genes_table)

	def write_files(self):
		# Write supermatrix FASTA and partition files, and link from report.
		html = []
		# FASTA file
		if self.check("superseq", "taxa"):
			with open(os.path.join(self.outdir, self.basename+".fa"), "w") as f:
				for taxon in self.data.taxa:
					print >>f, ">%s\n%s" % (taxon, self.data.superseq[taxon])
			html.append('[<a href="{0}.fa">FASTA</a>]')
		# partition file
		if self.check("seq_type", "genes", "gene_lengths"):
			if self.data.seq_type == "nt" or self.data.seq_type == "cds":
				partition_line = "DNA, %d = %d-%d"
			elif self.data.seq_type == "aa":
				partition_line = "WAG, %d = %d-%d"
			else:
				utils.die("unknown sequence type", self.data.seq_type)
			filename = os.path.join(self.outdir, self.basename+".partition.txt")
			with open(filename, "w") as f:
				i = 0
				for gene, length in izip(self.data.genes, self.data.gene_lengths):
					print >>f, partition_line % (gene, i+1, i+length)
					i += length
			html.append('[<a href="{0}.partition.txt">partition</a>]')
		if html:
			return [
				"<p>Files: ",
				" ".join(html).format(self.basename),
				"</p>"]

	def occupancy_table(self):
		if self.check("seq_type", "proportion", "occupancy", "gene_lengths"):
			if self.data.proportion == "None":
				self.data.proportion = 1.0
			total_occupancy = np.sum(self.data.occupancy.astype(bool)) / float(self.data.occupancy.size)
			rows = [
				("Sequence type", self.data.seq_type),
				("Target gene occupancy", "%.1f%%" % (100*float(self.data.proportion))),
				("Actual gene occupancy", "%.1f%%" % (100*total_occupancy)),
				("Number of genes", "{:,d}".format(len(self.data.occupancy))),
				("Number of columns", "{:,d}".format(sum(self.data.gene_lengths)))]
			return self.table(rows, style="lr")

	def occupancy_plot(self):
		"""
		Image of the gene occupancy in the supermatrix, ordered by most
		complete taxa, then most complete gene. Black indicates the gene is
		present, white that it is absent.
		"""
		if self.check("occupancy"):

			# Convert 1.0 to black, 0.0 to white
			occupancy = (-1.0 * self.data.occupancy.astype(bool).transpose()) + 1.0
			if occupancy.ndim == 1:
				occupancy = np.array([occupancy])

			# Plot matrix as grayscale image.
			return [self.imageplot(
				self.basename + ".png",
				occupancy,
				{
					"title": "Gene Occupancy",
					"xlabel": "Genes",
					"xticks": [],
					"ylabel": "Taxa",
					"yticks": [],
					"figsize": (9, 3)
				})]

	def cum_occupancy_plot(self):
		"""
		Plot of gene occupancies for cumulatively larger subsets of genes in
		the supermatrix, ordered by most complete gene.
		"""
		if self.check("occupancy", "taxa", "genes"):
			cum_occupancy = np.cumsum(np.sum(self.data.occupancy.astype(bool), axis=1), dtype=np.float64)
			cum_occupancy /= np.cumsum(len(self.data.taxa) * np.ones(len(self.data.genes)))

			# Cumulative occupancy
			return [self.lineplot(
				self.basename + ".cumalitve.png",
				cum_occupancy,
				{
					"title": "Cumulative Gene Occupancy",
					"xlabel": "Genes",
					"ylabel": "Occupancy",
					"ylim": [0.0, 1.05],
					"figsize": (9, 3)
				})]

	def taxon_genes_table(self):
		"""
		Number and percent of genes per taxon in supermatrix.
		"""
		if self.check("taxa", "occupancy"):
			taxa_occupancy = np.sum(self.data.occupancy.astype(bool), axis=0)
			perc = 100.0 / self.data.occupancy.shape[0]
			rows = []
			for taxon, ngenes in izip(self.data.taxa, taxa_occupancy):
				rows.append(
					(taxon, "%.0f" % ngenes, "%.1f%%" % (ngenes*perc)))
			headers = ("Species", "Number of genes", "Percent")
			return self.table(rows, headers, "lrr")

# vim: noexpandtab ts=4 sw=4
