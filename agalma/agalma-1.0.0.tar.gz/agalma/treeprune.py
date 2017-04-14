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
For each gene tree generated in genetree, prune the tree to include only one
representative sequence per taxon when sequences form a monophyletic group
(here called 'monophyly masking'). Then prune the monophyly-masked tree into
maximally inclusive subtrees with no more than one sequence per taxon (here
called 'paralogy pruning').

Use --previous for a specific set of trees, otherwise this pipeline will search
for the output from the most recent run of genetree for the given catalog ID.
"""

import os
import numpy as np

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline("treeprune", __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the trees from a previous run of genetree.""")

### STAGES ###

@pipe.stage
def init(id, previous):
	"""Determine path to input trees"""

	try:
		prev_id = diagnostics.lookup_prev_run(id, previous, "genetree").id
	except AttributeError:
		utils.die("no previous genetree run found for id", id)

	ingest("prev_id")


@pipe.stage
def prune_trees(prev_id):
	"""Prune each tree using monophyly masking and paralogy pruning"""

	pruned_trees = {}

	for id, newick in database.select_trees(prev_id):
		tree = workflows.phylogeny.tree(newick)
		masked_tree = workflows.phylogeny.monophyly_masking(tree)
		pruned_trees[id] = []
		workflows.phylogeny.paralogy_prune(masked_tree, pruned_trees[id])

	ingest("pruned_trees")


@pipe.stage
def parse_trees(_run_id, pruned_trees):
	"""Parse the tips of each tree to create a cluster in the database"""

	hist = {}
	nseqs = 0
	rows = []

	# Parse each paralogy pruned tree, and create a cluster from the tips
	for id in pruned_trees:
		for tree in pruned_trees[id]:
			tips = workflows.phylogeny.get_tips(tree)
			size = len(tips)
			# Only keep trees with 3 or more tips
			if size >= 3:
				hist[size] = hist.get(size, 0) + 1
				nseqs += size
				rows.append((id, tips))

	database.insert_pruned_homology(_run_id, rows)

	utils.info("histogram of gene cluster sizes:")
	for k in sorted(hist):
		print "%d\t:\t%d" % (k, hist[k])

	diagnostics.log("histogram", hist)
	diagnostics.log("nseqs", nseqs)


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
		self.lookup("histogram", "treeprune.parse_trees", "histogram")
		self.str2list("histogram")
		# Gener`ators
		self.generator(self.cluster_histogram)
		self.generator(self.threshold_table)

	def cluster_histogram(self):
		"""
		Distribution of the number of orthologs in each gene cluster.
		"""
		if self.check("histogram"):
			hist = self.data.histogram
			hist = [(k,hist[k]) for k in sorted(hist)]
			if len(hist) > 10:
				# Use a histogram
				imgname = "%d.cluster.hist.png" % self.run_id
				props = {
					"title": "Distribution of Cluster Sizes",
					"xlabel": "# Orthologs in Cluster",
					"ylabel": "Frequency"}
				return [self.histogram_overlay(imgname, [np.array(hist)], props=props)]
			else:
				# Use a table
				return self.table(hist, ("Cluster Size", "Frequency"))

	def threshold_table(self):
		"""

		"""
		sql = """
			SELECT size
			FROM agalma_homology
			WHERE run_id=?;"""
		genes = {}
		clusters = {}
		for row in database.execute(sql, (self.run_id,)):
			count = row[0]
			for i in xrange(3, count+1):
				genes[i] = genes.get(i, 0) + count
				clusters[i] = clusters.get(i, 0) + 1
		if genes:
			headers = ("Threshold", "# Clusters", "% Missing Genes")
			rows = []
			ntaxa = max(genes.iterkeys())
			for i in sorted(genes.iterkeys()):
				full = clusters[i] * ntaxa
				missing = 100.0 * (full - genes[i]) / full
				rows.append((str(i), str(clusters[i]), "%.1f%%" % missing))
			return self.table(rows, headers)

# vim: noexpandtab ts=4 sw=4
