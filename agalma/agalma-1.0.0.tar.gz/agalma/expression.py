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
Maps expression-only datasets to an assembly, estimates the read count for each
transcript in the assembly (at the gene and isoform level), and loads these
counts into the Agalma database.
"""

import csv
import os
import pandas as pd
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline("expression", __doc__)

### ARGUMENTS ###

pipe.add_arg("reference_id", metavar="REFERENCE_ID", help="""
	Run ID for the assembly/import to use as the reference, or a catalog ID to
	lookup the last assembly/import run for that catalog ID.""")

### STAGES ###

@pipe.stage
def setup_reference(reference_id):
	"""Locate reference sequences in the Agalma database"""

	try:
		reference_id = int(reference_id)
	except ValueError:
		pipelines = ("transcriptome", "assemble", "import")
		try:
			prev_run = diagnostics.lookup_prev_run(reference_id, None, *pipelines)
			reference_id = prev_run.id
			utils.info("using previous '%s' run id %s" % (prev_run.name, reference_id))
		except AttributeError:
			utils.die("no previous", '/'.join(pipelines), "runs found for id", reference_id)

	fasta = os.path.abspath("reference.fa")
	genemap = os.path.abspath("genemap.txt")
	database.export_gene_map(reference_id, fasta, genemap)
	workflows.assembly.stats(fasta)

	diagnostics.log_exit("reference_id", reference_id)
	ingest("fasta", "genemap", "reference_id")


@pipe.stage
def calculate(data, fasta, genemap):
	"""Calculate gene and isoform expression with RSEM"""
	wrappers.RsemReference(
		fasta, "rsem", "--transcript-to-gene-map", genemap)
	wrappers.RsemExpression(
		data[-1], "rsem", "rsem", "--no-bam-output --temporary-folder rsem.tmp")


@pipe.stage
def parse_counts(_run_id, reference_id):
	"""Parse gene-level counts into Agalma database"""
	rows = []
	for row in csv.DictReader(open("rsem.genes.results"), delimiter='\t'):
		rows.append((row["gene_id"], float(row["expected_count"])))
	database.insert_expression(_run_id, reference_id, rows)


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
		self.lookup("rsem", "expression.calculate.rsem-calculate-expression")
		self.lookup_attribute(diagnostics.EXIT, "reference_id")
		# Load types table
		self.data["types"] = database.select_model_types(self.data.reference_id)
		df = self.data.types
		self.data["types_table"] = pd.crosstab(df["genome_type"], df["molecule_type"])
		# Generators
		self.generator(self.rsem_table)
		self.generator(self.types_table)

	def rsem_table(self):
		if self.check("rsem"):
			return self.summarize(report.rsem_schema, "rsem")

	def types_table(self):
		"""
		Table showing classification of genome and molecule types for the
		sequences.
		"""
		if not self.data.types_table.empty:
			html = [
				self.header("Sequence Types"),
				'<table class="table table-striped table-condensed table-mini">',
				'<tr><td></td>']
			molecule_types = sorted(database.molecule_types)
			genome_types = sorted(database.genome_types)
			html += map('<td><b>{}</b></td>'.format, molecule_types)
			html.append('</tr>')
			for g in genome_types:
				html.append('</tr><td><b>{}</b></td>'.format(g))
				for m in molecule_types:
					try:
						html.append('<td>{:,g}</td>'.format(
							self.data.types_table[database.molecule_types[m]][database.genome_types[g]]))
					except KeyError:
						html.append('<td>0</td>')
				html.append('</tr>')
			html.append('</table>')
			return html

# vim: noexpandtab ts=4 sw=4
