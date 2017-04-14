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
Assembles reads into transcripts, processes the assembly, and generates
assembly diagnostics. Read pairs are first filtered at a more stringent
mean quality threshold. Transcriptome assembly is generated with Trinity
assembler.
"""

import csv
import hashlib
import numpy as np
import os
import pandas as pd
import re
from Bio import SeqIO

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline("assemble", __doc__)

trinity_header = re.compile(r"TRINITY_(DN\d+_c\d+_g\d+)_i(\d+)$")

### ARGUMENTS ###

pipe.add_arg("--quality", "-q", type=int, metavar="MIN", default=33, help="""
	Filter out reads that have a mean quality < MIN.""")

pipe.add_arg("--nreads", "-n", type=int, metavar="N", default=0, help="""
	Number of high quality reads to assemble (0 means all).""")

pipe.add_arg("--min_length", "-l", type=int, metavar="L", default=300, help="""
	Only keep transcripts longer than L nucleotides.""")

pipe.add_arg("--ss", default=None, help="""
	Specify orientation of strand-specific reads: FR or RF for paired, F or R
	for single-end. See the Trinity documentation for more details.""")

pipe.add_arg("--seed", "-s", default=None, help="""
	Use an explicit seed for RSEM-EVAL. [default: use a hash of the reads]""")


### STAGES ###

pipe.add_data_sources("rrna")

@pipe.stage
def setup_rrna(id, previous):
	"""Retrieve the rRNA exemplars from the database"""
	rrna_id = None
	try:
		rrna_id = diagnostics.lookup_prev_run(id, previous, "rrna").id
	except AttributeError:
		utils.info("no previous rrna run found for id", id)
	ingest("rrna_id")


@pipe.stage
def filter_data(id, data, quality, nreads):
	"""Filter out low-quality reads"""

	filtered = ["filtered.%d.fq" % i for i,_ in enumerate(data[-1])]
	wrappers.FilterIllumina(
				data[-1], filtered, "-a -b -q", quality, "-s / -n", nreads)
	data.append(filtered)
	log_state("data")


@pipe.stage
def assemble(id, data, min_length, ss):
	"""Assemble the filtered reads with Trinity"""

	args = ["--min_contig_length", min_length]
	if ss:
		args += ["--SS_lib_type", ss]
	wrappers.Trinity(data[-1], *args)
	assembly = "trinity_out_dir/Trinity.fasta"
	diagnostics.log_path(assembly)
	workflows.assembly.stats(assembly)
	ingest("assembly")


@pipe.stage
def parse_assembly(_run_id, id, assembly, ss):
	"""Parse the assembly into the sequences table"""

	strand = '+' if ss else '?'
	rows = []
	for record in SeqIO.parse(assembly, "fasta"):
		gene, isoform = trinity_header.match(record.id).groups()
		rows.append({
			"gene": gene,
			"isoform": isoform,
			"header": record.description,
			"sequence": str(record.seq)})
	database.insert_models(_run_id, id, 'n', rows, strand)
	parsed_assembly = "%s.fa" % id
	database.export_sequences(_run_id, parsed_assembly)
	ingest("parsed_assembly")


@pipe.stage
def remove_vectors(parsed_assembly):
	"""Remove vector contaminants with UniVec"""

	workdir = utils.safe_mkdir("univec")
	utils.safe_remove(os.path.join(workdir, "univec.log"))

	# Blastn against UniVec. This removes sequences that still have adapters,
	# or that are contaminated with plasmids (including the protein expression
	# plasmids used to manufacture sample prep enzymes).

	report = os.path.join(workdir, "out.txt")
	command = "blastn -evalue 0.0001 -outfmt '6 %s' -db %s -max_target_seqs 20" % (
				workflows.blast.tabular_fields_str,
				config.get_resource("univec_blastdb"))
	commands = workflows.blast.split_query(parsed_assembly, command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog univec.log --resume-failed --halt 1",
		stdout=report, cwd=workdir)

	rows = []
	for hit in workflows.blast.hits_tabular(os.path.join(workdir, report)):
		rows.append((
			database.get_genome_type(hit.stitle),
			hit.stitle,
			float(hit.evalue),
			int(hit.qseqid)))

	utils.info("found", len(rows), "vector contaminants")

	database.update_models(rows, "genome_type", "blast_title", "blast_evalue")


@pipe.stage
def remove_rrna(rrna_id, parsed_assembly):
	"""Remove rRNA using curated and exemplar sequences"""

	workdir = utils.safe_mkdir("rrna")
	utils.safe_remove(os.path.join(workdir, "rrna.log"))

	# Build database from the resource rRNAs and the exmplars.
	db_path = os.path.abspath("rrna.db")
	if rrna_id:
		utils.info("adding rRNA exemplars to blast database")
		database.export_sequences(rrna_id, db_path+".fa", "header")
	utils.cat_to_file(config.get_resource("rrna_fasta"), db_path+".fa")
	wrappers.MakeBlastDB(db_path+".fa", db_path, "nucl")

	# Blastn against rRNA, transferring sequences with or without a hit to
	# their own files.  Even when rRNA reads are removed prior to assembly,
	# some may make it through and be assembled from the full dataset
	# (including low frequency contaminant rRNAs).
	report = os.path.join(workdir, "out.txt")
	command = "blastn -evalue 0.0001 -outfmt '6 %s' -db %s -max_target_seqs 20" % (
				workflows.blast.tabular_fields_str, db_path)
	commands = workflows.blast.split_query(parsed_assembly, command, 100000, workdir)
	wrappers.Parallel(
		commands, "--joblog rrna.log --resume-failed --halt 1",
		stdout=report, cwd=workdir)

	rows = []
	for hit in workflows.blast.hits_tabular(os.path.join(workdir, report)):
		rows.append((
			database.get_genome_type(hit.stitle),
			database.get_molecule_type(hit.stitle),
			hit.stitle,
			float(hit.evalue),
			int(hit.qseqid)))

	utils.info("found", len(rows), "ribosomal RNAs")

	database.update_models(rows, "genome_type", "molecule_type", "blast_title", "blast_evalue")


@pipe.stage
def estimate_confidence(data, parsed_assembly, seed):
	"""Estimate coverage and confidence values for each transcript"""

	if seed is None:
		# Generate a 32-bit int from the first 64KB of the assembly
		seed = hashlib.md5()
		seed.update(open(parsed_assembly).read(65536))
		seed = str(int(seed.hexdigest(), 16) & 0xffffffff)
	diagnostics.log("seed", seed)

	wrappers.RsemEvalCalculateScore(data[-1], parsed_assembly, "rsem_eval", "--seed", seed)

	return {"scores": "rsem_eval.score.isoforms.results"}


@pipe.stage
def parse_confidence(scores):
	"""Parse estimated confidence scores and update database"""

	reader = csv.DictReader(open(scores), delimiter="\t")
	rows = []
	for line in reader:
		rows.append((
			float(line["expected_count"]),
			float(line["contig_impact_score"]),
			int(line["transcript_id"])))
	database.update_models(rows, "expression", "confidence")


### RUN ###

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

### REPORT ###

transcripts_schema = (
	report.Field('total', "Total transcripts", int, '{:,d}'),
	report.Field('nuclear-coding', "Nuclear/coding transcripts", int, '{:,d}'))

class Report(report.BaseReport):
	def init(self):
		self.name = pipe.name
		# Lookups
		self.lookup("filter", "assemble.filter_data.filter_illumina")
		self.percent("filter", "percent_kept", "pairs_kept", "pairs")
		if "filter" in self.data:
			# Pull the quality treshold out of the command arguments.
			self.data.filter["quality"] = self.extract_arg(
								"assemble.filter_data.filter_illumina", "-q")
		self.data["transcripts"] = {}
		self.data["coverage"] = database.select_model_coverage(self.run_id)
		df = self.data.coverage
		if not df.empty:
			self.data.transcripts["total"] = len(df["expression"])
		# Load types table
		self.data["types"] = database.select_model_types(self.run_id)
		df = self.data.types
		if not df.empty:
			self.data["types_table"] = pd.crosstab(df["genome_type"], df["molecule_type"])
			df = self.data.types_table
			try:
				self.data.transcripts["nuclear-coding"] = df[database.molecule_types["protein-coding"]][database.genome_types["nuclear"]]
			except KeyError:
				pass
		# Generators
		self.generator(self.filter_table)
		self.generator(self.types_table)
		self.generator(self.coverage_plot)
		self.generator(self.confidence_plot)
		self.generator(self.fasta)

	def filter_table(self):
		if "filter" in self.data:
			html = [self.header("Illumina Filtering")]
			html += self.summarize(report.filter_schema, "filter")
			return html

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

	def coverage_plot(self):
		if not self.data.coverage.empty:
			df = self.data.coverage.sort_values("expression", ascending=False)
			coverage = (
				df["expression"].cumsum(),
				df[df["annotated"]==1]["expression"].cumsum())
			imgname = '%d.assembly.coverage.svg' % self.run_id
			props = {
				"title": "Read Coverage across Transcripts",
				"xlabel": "Transcripts, ordered from highest to lowest representation",
				"ylabel": "Cumulative mapped reads (FPKM)"}
			plots = (
				(np.arange(coverage[0].size), coverage[0], "all transcripts"),
				(np.arange(coverage[1].size), coverage[1], "transcripts with blastx hits"))
			return [self.multilineplot(imgname, plots, props)]

	def confidence_plot(self):
		if not self.data.coverage.empty:
			df = self.data.coverage
			imgname = "%d.assembly.confidence.png" % self.run_id
			plt = df.plot(kind="scatter", x="expression", y="confidence")
			plt.get_figure().savefig(os.path.join(self.outdir, imgname))
			return [
				'<h4>Confidence vs. Expression</h4>',
				'<img src="%s" />' % imgname
			]

	def fasta(self):
		filename = "%d.assembly.fa" % self.run_id
		database.export_sequences(
			self.run_id,
			os.path.join(self.outdir, filename),
			"header")
		return [
			'<div class="well well-sm" style="text-align:center">',
			'<h4>Downloads</h4>',
			'<a href="%s" class="btn btn-lg btn-success">Assembly FASTA</a>' % filename,
			'</div>'
		]


# vim: noexpandtab ts=4 sw=4
