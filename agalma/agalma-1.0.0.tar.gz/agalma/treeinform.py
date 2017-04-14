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
For each gene tree generated in genetree, identify candidates for variants
of the same based on a treshold for branch lengths of subtrees. Then create a
new version in the genes table where the candidates are reassigned to the same
gene.
"""

import os
import numpy as np
from itertools import imap
from operator import itemgetter

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline("treeinform", __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the trees from a previous run of genetree.""")

pipe.add_arg("--threshold", "-t", type=float, default=0.05, help="""
	Subtrees with branch length less than THRESHOLD are candidates for
	variants of the same genes.""")

### STAGES ###

@pipe.stage
def init(id, previous):
	"""Determine path to input trees"""

	try:
		genetree_id = diagnostics.lookup_prev_run(id, previous, "genetree").id
	except AttributeError:
		utils.die("no previous genetree run for", id)
	utils.info("found genetree run", genetree_id)
	diagnostics.log("genetree_id", genetree_id)
	ingest("genetree_id")


@pipe.stage
def identify_candidate_variants(genetree_id, threshold):
	"""Identify candidates variants"""

	variants = {}
	trees = imap(itemgetter("tree"), database.select_trees(genetree_id))
	for i, model_ids in enumerate(workflows.phylogeny.identify_candidate_variants(trees, threshold)):
		for model_id in model_ids:
			assert model_id not in variants
			variants[model_id] = i

	ingest("variants")


@pipe.stage
def reassign_genes(_run_id, variants):
	"""Reassign candidate variants to the same gene"""

	genes = database.select_genes().fetchall()

	nreassigned = 0
	reassign = {}
	for row in genes:
		if row["model_id"] in variants:
			nreassigned += 1
			reassign[row["gene"]] = variants[row["model_id"]]

	rows = []
	for row in genes:
		if row["gene"] in reassign:
			rows.append((
				row["run_id"],
				row["model_id"],
				"REASSIGN.%d" % reassign[row["gene"]],
				row["isoform"]))
		else:
			rows.append(tuple(row))

	diagnostics.log("nreassigned", nreassigned)

	database.insert_genes(_run_id, rows)
	database.validate_genes(_run_id, len(variants))


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
		self.lookup("histogram", "treeinform.parse_trees", "histogram")
		self.str2list("histogram")
		# Generators
		self.generator(self.branch_length_histogram)

	def branch_length_histogram(self):
		"""
		Distribution of subtree branch lengths
		"""
		if self.check("histogram"):
			hist = self.data.histogram
			hist = [(k,hist[k]) for k in sorted(hist)]
			if len(hist) > 10:
				# Use a histogram
				imgname = "%d.branch.length.hist.png" % self.run_id
				props = {
					"title": "Distribution of Subtree Branch Lengths",
					"xlabel": "Branch Length",
					"ylabel": "Frequency"}
				return [self.histogram_overlay(imgname, [np.array(hist)], props=props)]
			else:
				# Use a table
				return self.table(hist, ("Branch Length", "Frequency"))

# vim: noexpandtab ts=4 sw=4
