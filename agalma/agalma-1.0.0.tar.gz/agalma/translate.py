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
Cleans transcripts to remove ribosomal, mitochondrial, vector, and
low-complexity sequences.  Vector sequences could include untrimmed adapters or
plasmids (we sometimes find sequences in our data for the protein expression
vectors used to manufacture the sample preparation enzymes).  Raw reads are
mapped back to the transcripts to estimate coverage and assign TPKM values.
Finally, transcripts are annotated with blast hits against SwissProt.
"""

import numpy as np
import os
import shutil
from Bio import SeqIO

from agalma import config
from agalma import database
from biolite import catalog
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import Pipeline

pipe = Pipeline("translate", __doc__)

### ARGUMENTS ###

pipe.add_arg("--previous", "-p", metavar="RUN_ID", default=None, help="""
	Use the sequences from a previous run of assemble or import.""")


### STAGES ###

@pipe.stage
def setup_sequences(id, previous):
	"""Locate a previous assemble or import run"""

	pipelines = ("assemble", "import")
	try:
		prev_run = diagnostics.lookup_prev_run(id, previous, *pipelines)
		utils.info("using previous '%s' run id %s" % (prev_run.name, prev_run.id))
	except AttributeError:
		utils.die("no previous", '/'.join(pipelines), "runs found for id", id)
	sequences = id+".fa"
	database.export_sequences(prev_run.id, sequences)
	ingest("sequences")


@pipe.stage
def identify_orfs(id, sequences):
	"""Identify long open reading frames"""

	wrappers.TransDecoderLongOrfs(sequences)
	orfs = os.path.join(sequences+".transdecoder_dir", "longest_orfs.pep")
	cds = os.path.join(sequences+".transdecoder_dir", "longest_orfs.cds")
	ingest("orfs", "cds")


@pipe.stage
def annotate_orfs(orfs):
	"""Blastp protein sequences against SwissProt"""

	workdir = os.path.abspath("blastp")
	command = "blastp -evalue 1e-6 -outfmt '6 %s' -db %s" % (
					workflows.blast.tabular_fields_str,
					config.get_resource('swissprot_blastdb'))
	commands = workflows.blast.split_query(orfs, command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog blastp.log --resume-failed --halt 1",
		stdout="blastp.tsv", cwd=workdir)

	hits = workflows.blast.top_hits_tabular("blastp.tsv")

	diagnostics.log("nhits", len(hits))

	ingest("hits")


@pipe.stage
def select_orfs(_run_id, orfs, hits, cds):
	"""Select the open reading frame with the best evalue"""

	# Choose annotation with the lowest evalue
	rows = {}
	for record in SeqIO.parse(orfs, "fasta"):
		model_id = int(record.id.partition('|')[0])
		if model_id not in rows:
			rows[model_id] = {
				"model_id": model_id,
				"orf_id": record.id,
				"header": record.description,
				"sequence": str(record.seq),
				"genome_type": database.genome_types["unknown"],
				"molecule_type": database.molecule_types["protein-coding"]}
		if record.id in hits:
			hit = hits[record.id]
			if float(hit.evalue) < rows[model_id].get("blast_evalue", 1.0):
				rows[model_id].update({
					"header": record.description,
					"sequence": str(record.seq),
					"genome_type": database.get_genome_type(hit.stitle),
					"blast_title": hit.stitle,
					"blast_evalue": float(hit.evalue)})

	fields = ("genome_type", "molecule_type", "blast_title", "blast_evalue", "model_id")
	database.update_models(
		[map(row.get, fields) for row in rows.itervalues()],
		*fields[:-1])

	seqs = [(row["model_id"], row["header"][-2], row["header"], row["sequence"]) for row in rows.itervalues()]
	database.update_sequences(seqs, _run_id, 'a')

	seqs = []
	for record in SeqIO.parse(cds, "fasta"):
		model_id = int(record.id.partition('|')[0])
		if model_id in rows and record.id == rows[model_id]["header"].partition(' ')[0]:
			seqs.append((model_id, record.description[-2], record.description, str(record.seq)))
	database.update_sequences(seqs, _run_id, 'c')


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
