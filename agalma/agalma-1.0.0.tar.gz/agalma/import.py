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
Imports nucleotide or amino acid sequences into Agalma's database. Optionally,
also uses the annotations for amino acid sequences that were downloaded from
NCBI.
"""

import os
from Bio import SeqIO

from agalma import config
from agalma import database
from biolite import catalog
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite.pipeline import Pipeline

pipe = Pipeline("import", __doc__)

### ARGUMENTS ###

pipe.add_arg("paths", nargs="*", default=None, metavar="FASTA", help="""
	Paths of FASTA files containing the sequences to import.""")

pipe.add_arg("--seq_type", default="nt", help="""
	Imported sequences are "nt" (nucleotide), "cds" (coding sequence), or "aa"
	(amino acid).""")

pipe.add_arg("--annotated", action="store_true", default=False, help="""
	The aa sequences are already annotated with the top blast hit in the
	FASTA header.""")


### STAGES ###

@pipe.stage
def setup_paths(id, paths):
	"""Determine the paths to the FASTA files"""
	if not paths:
		try:
			paths = catalog.split_paths(catalog.select(id).paths)
		except AttributeError:
			utils.die("catalog entry missing for id", id)
	paths = map(os.path.abspath, paths)
	utils.info("found paths", str(paths))
	ingest("paths")


@pipe.stage
def parse_sequences(_run_id, id, paths, seq_type, annotated):
	"""Parse the sequences from the FASTA files"""

	if seq_type not in ("aa", "cds", "nt"):
		utils.die("unknown sequence type", seq_type)

	rows = []
	for path in paths:
		for record in SeqIO.parse(path, "fasta"):
			row = {
				"sequence": str(record.seq),
				"header": record.description,
				"isoform": 1
			}
			if annotated:
				row["gene"] = record.id.strip('|')
				row["blast_title"] = record.description
			else:
				row["gene"] = record.id
			rows.append(row)

	if annotated:
		database.insert_models(
			_run_id, id, seq_type[0], rows,
			molecule_type=database.molecule_types["protein-coding"],
			genome_type=database.genome_types["nuclear"])
	else:
		database.insert_models(_run_id, id, seq_type[0], rows)


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
