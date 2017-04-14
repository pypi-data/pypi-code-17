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
Applies sampling and length filters to each cluster of homologous sequences.

Creates multiple sequence alignments for each cluster of homologous sequences
using MAFFT using the E-INS-i algorithm; see doi: 10.1093/molbev/mst010.

Cleans up alignments using Gblocks.
"""

import math
import os
from Bio import SeqIO
from collections import namedtuple
from operator import attrgetter

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline("multalign", __doc__)

# Data struct for a cluster of homologous sequences
Cluster = namedtuple("Cluster", "id size weight fasta")

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the homologous sequences from a previous run of homologize
	or treeprune.""")

pipe.add_arg("--seq_type", default="aa", help="""
	Choose whether alignments are based on "nt" (nucleotide), "cds" (coding
	sequence), or "aa" (amino acid) sequences.""")

pipe.add_arg("--min_taxa", type=int, default=4, help="""
	Minimum number of taxa required to retain a cluster.""")

pipe.add_arg("--max_sequences", type=int, default=300, help="""
	Maximum number of sequences to allow in a cluster.""")

pipe.add_arg("--max_length", type=int, default=10000, help="""
    Maximum length for sequences in a cluster.""")

pipe.add_arg("--min_length", type=int, default=50, help="""
	Minimum length for a clean alignment.""")

pipe.add_arg("--min_sites", type=int, default=20, help="""
	Minimum number of non-ambiguous sites required to retain a sequence in
	the clean alignment.""")

### STAGES ###

@pipe.stage
def init(id, previous):
	"""Locate a previous homology or treeprune run"""

	pipelines = ("homologize", "treeprune")
	try:
		prev_run = diagnostics.lookup_prev_run(id, previous, *pipelines)
		utils.info("using previous '%s' run id %s" % (prev_run.name, prev_run.id))
	except AttributeError:
		utils.die("no previous", '/'.join(pipelines), "runs found for id", id)

	return {"prev_id": int(prev_run.id)}


@pipe.stage
def select_clusters(
	_run_id, prev_id, seq_type, min_taxa, max_sequences, max_length):
	"""
	Select a cluster for each homologize component that meets size, sequence
	length, and composition requirements
	"""

	if seq_type not in ("nt", "cds", "aa"):
		utils.die("unknown sequence type:", seq_type)

	nseqs = {
		"max_length": 0,
		"max_sequences": 0,
		"min_taxa": 0,
		"taxa_mean": 0 }

	cluster_dir = utils.safe_mkdir("clusters")
	clusters = []
	for homology_id, sequences in database.select_homology_models(prev_id, seq_type[0], max_length):
		# Apply filter on cluster size
		size = len(sequences)
		nseqs["max_length"] += size
		if size <= max_sequences:
			nseqs["max_sequences"] += size
			# Count the number of times a taxon is repeated in the cluster
			# and calculate the cluster weight
			taxa_count = {}
			weight = 0
			for taxon, _, seq in sequences:
				taxa_count[taxon] = taxa_count.get(taxon, 0) + 1
				weight += len(seq)
			# Weight is an approximation of how many comparisons need to be
			# performed in multiple alignment, for ordering from most
			# computational to least
			weight = (weight / size) ** size
			# Compute the mean number of repetitions
			taxa_count = taxa_count.values()
			taxa_mean = sum(taxa_count) / float(len(taxa_count))
			# Require at least min_taxa, and that the mean reptitions is less
			# than 5.
			if len(taxa_count) >= min_taxa:
				nseqs["min_taxa"] += size
				if taxa_mean < 5:
					nseqs["taxa_mean"] += size
					fasta = os.path.join(cluster_dir, "%d.fa" % homology_id)
					with open(fasta, "w") as f:
						for record in sequences:
							print >>f, ">%s@%d\n%s" % record
					clusters.append(Cluster(homology_id, size, weight, [fasta]))

	diagnostics.log_entity("max_length.nseqs", nseqs["max_length"])
	diagnostics.log_entity("max_sequences.nseqs", nseqs["max_sequences"])
	diagnostics.log_entity("min_taxa.nseqs", nseqs["min_taxa"])
	diagnostics.log_entity("taxa_mean.nseqs", nseqs["taxa_mean"])

	if not clusters:
		utils.die("no clusters passed the filtering criteria")

	ingest("clusters")


@pipe.stage
def align_sequences(clusters, seq_type):
	"""Align sequences within each component"""

	align_dir = utils.safe_mkdir("alignments")

	if seq_type == "nt" or seq_type == "cds":
		type_flag = "--nuc"
	elif seq_type == "aa":
		type_flag = "--amino"
	else:
		utils.die("invalid sequence type:", seq_type)

	# Sort by descending size to improve load balancing
	with open("align.sh", 'w') as f:
		for cluster in sorted(clusters, key=attrgetter("weight"), reverse=True):
			aligned = os.path.join(align_dir, "%d.fa" % cluster.id)
			print >>f, "%s %s --thread %s --ep 0 --genafpair --maxiterate 10000 --anysymbol %s > %s" % (
				config.get_command("mafft")[0], type_flag,
				config.get_resource("threads"), cluster.fasta[-1], aligned)
			cluster.fasta.append(aligned)

	wrappers.Parallel(
		"align.sh", "--joblog align.log --resume-failed --halt 1", threads=1)


@pipe.stage
def cleanup_alignments(clusters, seq_type):
	"""Clean up aligned sequences with Gblocks"""

	t = seq_type[0].replace('n', 'd').replace('c', 'd')

	with open("cleanup.sh", 'w') as f:
		for cluster in clusters:
			print >>f, "%s %s -t=%s -b2=%.0f -b3=10 -b4=5 -b5=a" % (
				config.get_command("Gblocks")[0], cluster.fasta[-1],
				t, math.ceil(0.65*cluster.size))

	wrappers.Parallel(
		"cleanup.sh", "--joblog cleanup.log --resume", return_ok=None)


@pipe.stage
def parse_alignments(_run_id, clusters, min_length, min_sites, min_taxa):
	"""Parse the cleaned sequences into the database"""

	nseqs = 0
	nlength = 0
	nsites = 0
	ntaxa = 0

	rows = []
	for cluster in clusters:
		if not os.path.exists(cluster.fasta[-1]+"-gb"):
			utils.info("alignment failed for cluster", cluster.id)
			continue
		# Parse Gblocks output
		keep = []
		for record in SeqIO.parse(cluster.fasta[-1]+"-gb", "fasta"):
			# Skip short clusters
			if len(record.seq) < min_length:
				nlength += cluster.size
				break
			# Keep sequences that have the required number of non-ambiguous sites
			if sum(1 for c in record.seq if c != '-') >= min_sites:
				keep.append(">%s\n%s\n" % (record.description, record.seq))
			else:
				nsites += 1
				utils.info(
					"dropping sequence", record.description,
					"in cluster", cluster.id)

		# Clusters must have at least size min_taxa to be meaningful gene trees
		if len(keep) < min_taxa:
			ntaxa += len(keep)
			utils.info("dropping cluster", cluster.id)
		else:
			nseqs += cluster.size
			rows.append((cluster.id, "\n".join(keep)))

	database.insert_alignments(_run_id, rows)

	diagnostics.log("nseqs", nseqs)
	diagnostics.log("nlength", nlength)
	diagnostics.log("nsites", nsites)
	diagnostics.log("ntaxa", ntaxa)


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
		# Generators

# vim: noexpandtab ts=4 sw=4
