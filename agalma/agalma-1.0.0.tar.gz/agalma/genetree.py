# Agalma - an automated phylogenomics workflow
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
Builds gene trees for each alignment of homologous sequences, it builds a
phylogenetic tree using the maximum likelihood optimality criterion as
implemented in RAxML (see http://www.exelixis-lab.org/ and
doi:10.1093/bioinformatics/btl446).

Use --previous for a specific set of alignments, otherwise this pipeline will
search for the output from the most recent run of multalign for the given
catalog ID.
"""

import os
from csv import DictReader

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline("genetree", __doc__)

### ARGUMENTS ###

aa_models = ("PROTCATWAG", "PROTCATLG", "PROTGAMMAWAG", "PROTGAMMALG")
nt_models = ("GTRMIX", "GTRCAT", "GTRGAMMA")

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the alignments from a previous multalign run.""")

pipe.add_arg("--model", "-m", default="PROTGAMMAWAG", help="""
	The substitution model of evolution for RAxML.
	Protein models: %s
	Nucleotide models: %s""" % (str(aa_models), str(nt_models)))

pipe.add_arg("--bootstrap", "-b", type=int, default=0, help="""
	Number of bootstrap replicates to run for RAxML.""")

### STAGES ###

@pipe.stage
def init(id, model, previous):
	"""Find alignments in database"""

	try:
		prev_id = diagnostics.lookup_prev_run(id, previous, "multalign").id
	except AttributeError:
		utils.die("no previous multalign runs found for id", id)

	seq_type = diagnostics.lookup(prev_id, diagnostics.INIT)["seq_type"]
	if seq_type == "aa" and model not in aa_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))
	elif (seq_type == "nt" or seq_type == "cds") and model not in nt_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))

	ingest("prev_id", "seq_type")


@pipe.stage
def genetrees(prev_id, model, bootstrap):
	"""Build gene trees from alignments"""

	align_dir = utils.safe_mkdir("alignments")
	tree_dir = utils.safe_mkdir("trees")
	alignments = []

	with open("raxml.sh", 'w') as f:
		for id, fasta in database.select_alignments(prev_id):
			command = config.get_command("raxml")
			alignments.append(id)
			alignment = os.path.join(align_dir, "%d.fa" % id)
			open(alignment, 'w').write(fasta)
			seed = str(utils.md5seed(alignment) % 10000000000)
			tree = os.path.join(tree_dir, "%d.newick" % id)
			command += ["-s", alignment, "-n", str(id), "-m", model, "-p", seed, "-w /tmp"]
			if bootstrap:
				command += ["-x", seed, "-f a -#", str(bootstrap)]
			rm = "rm -f /tmp/RAxML_*.%d" % id
			raxml = " ".join(command)
			if bootstrap:
				mv = "mv /tmp/RAxML_bipartitions.%d %s" % (id, tree)
			else:
				mv = "mv /tmp/RAxML_bestTree.%d %s" % (id, tree)
			print >>f, " && ".join((rm, raxml, mv))

	wrappers.Parallel("raxml.sh --joblog raxml.log --halt 1 --resume")

	ingest("tree_dir", "alignments")


@pipe.stage
def parse(_run_id, tree_dir, alignments):
	"""Parse the trees into the database. Check for jobs that timed out."""

	rows = []
	for id in alignments:
		tree = os.path.join(tree_dir, "%d.newick" % id)
		if os.path.exists(tree) and os.path.getsize(tree):
			rows.append((id, open(tree).read()))

	database.insert_trees(_run_id, rows)


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

# vim: noexpandtab ts=4 sw=4
