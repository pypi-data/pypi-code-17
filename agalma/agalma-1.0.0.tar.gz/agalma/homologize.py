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
Identifies homologous sequences across datasets. Takes assembly or group of
assemblies and prepares a set of comprehensive comparisons between them. First
an all by all BLAST is run with a stringent threshold, and the hits which match
above a given score are used as edges between two transcripts which then form a
graph. This graph is the basis of a series of comparative scores.
"""

import os
import numpy as np
import threading

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline("homologize", __doc__)

### ARGUMENTS ###

pipe.add_arg("--seq_type", "-t", metavar="TYPE", default="aa", help="""
	Choose whether comparisons are based on "nt" (nucloetide), "cds" (coding
	sequence), or "aa" (amino acid) sequences.""")

pipe.add_arg(
	"--genome_type", "-g", nargs="+", metavar="TYPE",
	default=["nuclear"], help="""
		Select sequences with genome type: nuclear, mitochondrial, and/or
		plastid.""")

pipe.add_arg(
	"--molecule_type", "-m", nargs="+", metavar="TYPE",
	default=["protein-coding"], help="""
		Select sequences with molecule type: protein-coding, ribosomal-small,
		ribosomal-large, ribosomal, and/or unknown.""")

pipe.add_arg("--min_bitscore", type=float, default=200, help="""
	Filter out BLAST hit edges with a bitscore below min_bitscore.""")

pipe.add_arg("--min_overlap", type=float, default=0.5, help="""
	Filter out BLAST hit edges with a max HSP length less than this fraction
	of target length.""")

pipe.add_arg("--min_nodes", type=int, default=4, help="""
	Minimum number of nodes to be retained as a homolgous gene cluster.""")

pipe.add_path_arg("--genesets", nargs="+", default=None, help="""
	Concatenate the specified amino acid FASTAs and use as the reference for
	a blastx or blastp comparison, instead of performing an all-to-all
	comparison. FASTA headers must start with a non-digit.""")

pipe.add_path_arg("--blast_hits", default=None, help="""
	Use a pre-computed blast alignment when starting from the parse_edges
	stage.""")


### STAGES ###

@pipe.stage
def init(id, _run_id):
	"""Determine the version of gene entries to use and lookup species data"""

	genes_version = database.latest_genes_version(id)
	database.store(_run_id, "species", database.select_species(genes_version))
	ingest("genes_version")


@pipe.stage
def write_fasta(genes_version, seq_type, molecule_type, genome_type):
	"""Write sequences from the Agalma database to a FASTA file"""

	blast_dir = utils.safe_mkdir("blastp")
	fasta = os.path.join(blast_dir, "all.fa")

	if "any" in genome_type: genome_type = None
	if "any" in molecule_type: molecule_type = None

	nseqs = database.export_exemplars(genes_version, fasta, seq_type, molecule_type, genome_type)

	if not nseqs:
		utils.die("no sequences were written to the FASTA file")

	diagnostics.log_path(fasta, "fasta")
	diagnostics.log("nseqs", nseqs)

	ingest("blast_dir", "fasta")


@pipe.stage
def prepare_blast(blast_dir, fasta, seq_type, genesets):
	"""Prepare all-by-all BLAST database and command list"""

	db = os.path.join(blast_dir, "db")

	if genesets:
		if seq_type == "aa":
			program = "blastp"
		else:
			program = "blastx"
		for geneset in genesets:
			utils.cat_to_file(geneset, db+".fa")
			# Also add genesets to the query file, to find overlapping genes
			# between sets.
			utils.cat_to_file(geneset, fasta)
		wrappers.MakeBlastDB(db+".fa", db, "prot")
	else:
		if seq_type == "aa":
			dbtype = "prot"
			program = "blastp"
		elif seq_type == "nt" or seq_type == "cds":
			dbtype = "nucl"
			program = "tblastx"
		else:
			utils.die("unrecognized sequence type:", seq_type)
		wrappers.MakeBlastDB(fasta, db, dbtype)

	command = program + " -db db -evalue 1e-20" \
	                  + " -outfmt \"6 qseqid sseqid bitscore qlen length\""
	commands = workflows.blast.split_query(fasta, command, 100000, blast_dir)

	ingest("commands")


@pipe.stage
def run_blast(blast_dir, commands):
	"""Run all-by-all BLAST"""
	blast_hits = os.path.join(blast_dir, "hits.tab")
	wrappers.Parallel(
		commands, "--joblog blast.log --resume-failed --halt 1",
		stdout=blast_hits, cwd=blast_dir)
	ingest("blast_hits")


@pipe.stage
def parse_edges(_run_id, seq_type, blast_hits, min_overlap, min_bitscore, min_nodes):
	"""Parse BLAST hits into edges weighted by bitscore"""

	pipe_file = utils.make_pipe()
	mci_file = "edges.mci"

	mcxload = threading.Thread(
				target=wrappers.Mcxload,
				args=(
					"-abc", pipe_file,
					"-ri max --write-binary",
					"-o {0} -write-tab {0}.tab".format(mci_file)))
	mcxload.start()

	seqs = set()
	nedges = {
		"all": 0,
		"non-self": 0,
		"passed-overlap": 0,
		"passed-bitscore": 0}

	with open(pipe_file, "w") as pipe:
		for line in open(blast_hits):
			# Blast prints warnings into stdout
			if not line[0].isdigit():
				continue
			# fields:
			# qseqid sseqid bitscore qlen length
			id_from, id_to, bitscore, qlen, length = line.rstrip().split()
			# Skip rows that don't correspond to the specified ids
			id_from = int(id_from)
			id_to = int(id_to)
			seqs.add(id_from)
			seqs.add(id_to)
			bitscore = float(bitscore)
			length = float(length) / float(qlen)
			# Correct for nucleotide vs. amino acid length
			if seq_type == "nucleotide":
				length *= 3.0
			# Filter out self hits, low scoring hits, and short hits
			nedges["all"] += 1
			if id_from != id_to:
				nedges["non-self"] += 1
				if length > min_overlap:
					nedges["passed-overlap"] += 1
					if bitscore > min_bitscore:
						nedges["passed-bitscore"] += 1
						print >>pipe, "%d\t%d\t%g" % (id_from, id_to, bitscore)

	mcxload.join()

	diagnostics.prefix.append("nedges")
	diagnostics.log_dict(nedges)
	diagnostics.prefix.pop()

	if not seqs:
		utils.die("no sequences were written to the FASTA file")

	diagnostics.log("nseqs", len(seqs))

	ingest("mci_file")


@pipe.stage
def mcl_cluster(mci_file):
	"""Run mcl on all-by-all graph to form gene clusters"""
	cluster_file = "mcl_clusters.abc"
	wrappers.Mcl(mci_file, "-I 2.1 -use-tab %s.tab" % mci_file, "-o", cluster_file)
	ingest("cluster_file")


@pipe.stage
def load_mcl_cluster(_run_id, cluster_file, min_nodes):
	"""Load cluster file from mcl into homology database"""

	rows = []
	nseqs = 0
	hist = {}

	with open(cluster_file, 'r') as f:
		cluster_id = 0
		for line in f:
			cluster = filter(lambda s : s[0].isdigit(), line.rstrip().split())
			size = len(cluster)
			hist[size] = hist.get(size, 0) + 1
			if size >= min_nodes:
				nseqs += size
				rows.append(cluster)

	database.insert_homology(_run_id, rows)

	utils.info(
		"histogram of gene cluster sizes:\n",
		'\n '.join("%d\t:\t%d" % (k, hist[k]) for k in sorted(hist)))

	diagnostics.log("nseqs", nseqs)
	diagnostics.log("histogram", hist)


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
		# Lookups
#		self.retrieve("species")
		self.lookup("nseqs", "homologize.write_fasta", "nseqs")
		# Generators
		self.generator(self.species_table)
		self.generator(self.cluster_histogram)

	def species_table(self):
		"""
		Summary of all species processed.
		"""
		html = []
		if self.check("nseqs"):
			html.append("<p>Total sequences: %s</p>" % self.data.nseqs)
		if self.check("species"):
			headers = ("Models Run ID", "Catalog ID", "Species", "NCBI ID", "ITIS ID")
			html += self.table(self.data.species, headers)
		return html

	def cluster_histogram(self):
		"""
		Distribution of the number of nodes in each cluster.
		"""
		hist = database.count_homology(self.run_id)
		if hist:
			imgname = "%d.cluster.hist.png" % self.run_id
			props = {
				"title": "Distribution of Cluster Sizes",
				"xlabel": "# Nodes in Cluster",
				"ylabel": "Frequency"}
			return [self.histogram_overlay(imgname, [np.array(hist)], props=props)]

# vim: noexpandtab ts=4 sw=4
