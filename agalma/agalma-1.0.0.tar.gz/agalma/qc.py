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
Quality control for raw Illumina reads using FastQC.
"""

import os

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline("qc", __doc__)

### ARGUMENTS ###


### STAGES ###

@pipe.stage
def fastqc(id, data):
	"""Generate FastQC reports for each FASTQ file"""

	names = []
	for i, fastq in enumerate(data[-1]):
		wrappers.FastQC(fastq, "--extract -f fastq -o", os.getcwd())
		names.append(utils.basename(fastq) + "_fastqc")
	ingest("names")


@pipe.stage
def parse(_run_id, data, names):
	"""Parse FastQC reports into the database"""

	reports = [open(n + ".html").read() for n in names]
	database.store(_run_id, "reports", reports)

	summaries = [open(os.path.join(n, "summary.txt")).read() for n in names]
	database.store(_run_id, "summaries", summaries)


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
		self.retrieve("reports")
		self.retrieve("summaries")
		# Generators
		self.generator(self.fastqc_table)

	def fastqc_table(self):
		"""
		FastQC_ is a tool from Babraham Bioinformatics that generates detailed
		quality diagnostics of NGS sequence data.

		.. _FastQC: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
		"""
		if self.data.reports and self.data.summaries:
			n = len(self.data.reports)
			summaries = [s.strip().split("\n") for s in self.data.summaries]
			rows = [r.split("\t")[1] for r in summaries[0]]
			cells = [[r.split("\t")[0] for r in s] for s in summaries]
			colors = {
				"PASS": "green",
				"WARN": "orange",
				"FAIL": "red"}
			html = [
				self.header("FastQC Summary"),
				'<table class="table">',
				'<tr><th></th>']
			for i in xrange(n):
				report = os.path.join(self.outdir, "fastqc{}.html".format(i+1))
				open(report, "w").write(self.data.reports[i])
				html.append(
					'<th>FASTQ {0} (<a href="fastqc{0}.html">full report</a>)</th>'.format(i+1))
			html.append('</tr>')
			for j, row in enumerate(rows):
				html.append("<tr><th>%s</th>" % row)
				for i in xrange(n):
					html.append('<td><span style="color:{};">{}</span></td>'.format(
							colors[cells[i][j]],
							cells[i][j]))
				html.append('</tr>')
			html.append('</table>')
			return html

# vim: noexpandtab ts=4 sw=4
