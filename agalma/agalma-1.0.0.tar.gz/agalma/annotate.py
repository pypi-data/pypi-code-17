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
Annotate protein sequences with blast hits against SwissProt and output an annotated
FASTA file in Agalma format.
"""

import os

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline("annotate", __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the sequences from a previous run of import.""")


### STAGES ###

@pipe.stage
def setup_sequences(id, previous):
	"""Locate a previous import run"""
	try:
		prev_run = diagnostics.lookup_prev_run(id, previous, "import")
		utils.info("using previous '%s' run id %s" % (prev_run.name, prev_run.id))
	except AttributeError:
		utils.die("no previous import run found for", id)
	sequences = id+".fa"
	database.export_sequences(prev_run.id, sequences, seq_type='a')
	ingest("sequences")


@pipe.stage
def annotate(sequences):
	"""Blastp protein sequences against SwissProt"""
	workdir = os.path.abspath("blastp")
	command = "blastp -evalue 1e-6 -outfmt '6 %s' -db %s" % (
					workflows.blast.tabular_fields_str,
					config.get_resource('swissprot_blastdb'))
	commands = workflows.blast.split_query(sequences, command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog blastp.log --resume-failed --halt 1",
		stdout="blastp.tsv", cwd=workdir)


@pipe.stage
def parse():
	"""Parse the annotations into the sequences table"""
	rows = []
	for hit in workflows.blast.hits_tabular("blastp.tsv"):
		rows.append((
				database.get_genome_type(hit.stitle),
				database.molecule_types["protein-coding"],
				hit.stitle,
				float(hit.evalue),
				int(hit.qseqid.partition('|')[0])))
	diagnostics.log("nhits", len(rows))
	database.update_models(
				rows,
				"genome_type", "molecule_type", "blast_title", "blast_evalue")


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
