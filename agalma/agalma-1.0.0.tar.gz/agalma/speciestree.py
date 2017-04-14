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
Builds a species tree from a supermatrix.
"""

import os
import random
import sys
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline("speciestree", __doc__)

### ARGUMENTS ###

prot_models = ("PROTCATWAG", "PROTCATLG", "PROTGAMMAWAG", "PROTGAMMALG")
nuc_models = ("GTRMIX", "GTRCAT", "GTRGAMMA")

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the alignment from a previous run of supermatrix.""")

pipe.add_arg("--model", "-m", default="PROTGAMMAWAG", help="""
	The substitution model of evolution for RAxML.
	Protein models: %s
	Nucleotide models: %s""" % (str(prot_models), str(nuc_models)))

pipe.add_arg("--bootstrap", "-b", type=int, default=0, help="""
	Number of bootstrap replicates to run for RAxML.""")

pipe.add_arg("--seed", "-s", default=None, help="""
	Use an explicit seed, used to generate additional random seeds for
	RAxML runs. [default: use a hash of the supermatrix]""")

pipe.add_arg("--outgroup", "-g", nargs="+", default=None, help="""
	Put the node with the provided taxon label in the outgroup position.""")

pipe.add_arg("--raxml_flags", "-f", default="", help="""
	Extra parameters to pass to RAxML. Make sure the flags make sense: refer to
	the RAxML Manual for help.""")

pipe.add_arg("--mpi", metavar="MPIRUN", default="", help="""
	Run RAxML in MPI mode using the specified MPIRUN command.""")

pipe.add_arg("--hybrid", action="store_true", default=False, help="""
	Specify in addition to --mpi to Run RAxML in MPI-hybrid mode.""")

### STAGES ###

@pipe.stage
def init(id, model, previous):
	"""Find supermatrix in database"""

	try:
		prev_id = diagnostics.lookup_prev_run(id, previous, "supermatrix").id
	except AttributeError:
		utils.die("no previous supermatrix runs found for id", id)

	alignment = "alignment.fa"
	with open(alignment, "w") as f:
		for row in database.retrieve(prev_id, "superseq").iteritems():
			print >>f, ">%s\n%s" % row

	seq_type = diagnostics.lookup(prev_id, diagnostics.EXIT)["seq_type"]

	if seq_type == "aa" and model not in prot_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))
	elif seq_type == "nt" and model not in nuc_models:
		utils.die(
			"%s is not a valid model for %s sequences" % (model, seq_type))

	ingest("alignment", "seq_type")


@pipe.stage
def speciestree(
		alignment, seq_type, model, bootstrap, seed, outgroup, raxml_flags,
		mpi, hybrid):
	"""Build species tree with bootstraps"""

	if seed is None:
		seed = utils.md5seed(alignment)

	args = ["-n", alignment, "-m", model, "-w", os.getcwd(), "-p", seed]
	if outgroup:
		args += ["-o", ','.join(outgroup)]
	if bootstrap > 0:
		args += ["-f a -#", bootstrap, "-x", seed]
	args.append(raxml_flags)

	# Run RAxML
	if mpi:
		if hybrid:
			wrappers.RaxmlHybrid(mpi, alignment, *args)
		else:
			wrappers.RaxmlMpi(mpi, alignment, *args)
	else:
		wrappers.Raxml(alignment, *args)


@pipe.stage
def parse(_run_id, alignment, bootstrap):
	"""Parse the tree into the database"""
	if bootstrap:
		tree = open("RAxML_bipartitions." + alignment).read()
	else:
		tree = open("RAxML_bestTree." + alignment).read()
	utils.info("species tree:\n" + workflows.phylogeny.ascii_plot(tree))
	database.store(_run_id, "tree", tree)


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
		self.retrieve("tree")
		# Generators
		self.generator(self.plot_tree)

	def plot_tree(self):
		"""
		Maximum-likelihood tree for the supermatrix.
		"""
		if self.check("tree"):
			self.add_js("d3.v3.min.js")
			self.add_js("newick.js")
			self.add_js("d3.phylogram.js")
			return ["""
				<div id="run_{0}_canvas"></div>
				<pre id="run_{0}_newick_text" onclick="selectText(this)">{1}</pre>
				<script type="text/javascript">
					var run_{0}_newick = Newick.parse("{1}");
					var newickNodes = []
					function buildNewickNodes(node, callback) {{
						newickNodes.push(node)
						if (node.branchset) {{
							for (var i=0; i < node.branchset.length; i++) {{
								buildNewickNodes(node.branchset[i])
							}}
						}}
					}}
					buildNewickNodes(run_{0}_newick);
						
					d3.phylogram.build("#run_{0}_canvas", run_{0}_newick, {{
						width: 800,
						height: 800
					}});

					function selectText(elem) {{
						if (document.selection) {{
							var range = document.body.createTextRange();
							range.moveToElementText(elem);
							range.select();
						}} else if (window.getSelection) {{
							var range = document.createRange();
							range.selectNode(elem);
							window.getSelection().addRange(range);
						}}
					}}
				</script>
				""".format(self.run_id, self.data.tree.strip())]

# vim: noexpandtab ts=4 sw=4
