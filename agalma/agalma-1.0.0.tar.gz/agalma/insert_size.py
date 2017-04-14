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
Estimates the insert size distribution of paired-end Illumina data by
assembling a subset of the data and mapping read pairs to it. The insert
size does not include the adapters added during library preparation.
"""

import os

from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline("insert_size", __doc__)

### ARGUMENTS ###

pipe.add_arg("--quality", "-q", type=int, metavar="MIN", default=33, help="""
	Use reads with mean quality > MIN.""")

pipe.add_arg("--nreads", "-n", type=int, metavar="N", default=100000, help="""
	Number of high quality reads to use.""")

pipe.add_arg("--ss", default=None, help="""
	Specify orientation of strand-specific reads: FR or RF for paired, F or R
	for single-end. See the Trinity documentation for more details.""")

### STAGES ###

@pipe.stage
def assemble_subset(data, quality, nreads, ss):
	"""Assemble a subset of high quality reads"""

	# Create a subset of n high-quality reads
	subset = ["subset.%d.fq" % i for i in xrange(len(data[-1]))]
	wrappers.FilterIllumina(
				data[-1], subset, "-q", quality, "-n", nreads, "-a")

	name = "trinity_%d" % nreads

	# Assemble the subset
	args = ["--min_contig_length 300 --full_cleanup --output", name]
	if ss:
		args += ["--SS_lib_type", ss]
	wrappers.Trinity(subset, *args)

	return {
		"subset": subset,
		"assembly": name+".Trinity.fasta"}


@pipe.stage
def estimate_insert(_run_id, data, subset, assembly):
	"""Estimate insert size by mapping the subset against the assembly"""

	wrappers.Bowtie2Build(assembly, assembly)

	histfile = "insert_hist.txt"
	insert_cmd = "%s -o %s -m %s" % (
								config.get_command("insert_stats")[0],
								histfile,
								config.get_resource("max_insert_size"))

	wrappers.Bowtie2(
				subset, assembly,
				"--very-sensitive-local --no-unal --no-mixed",
				"--no-discordant --no-dovetail --no-contain",
				pipe=insert_cmd)

	# check insert size
	stats = diagnostics.local_lookup("insert_size.estimate_insert.bowtie2")
	try:
		mean = int(float(stats["mean"]))
		stddev = int(float(stats["stddev"]))
	except ValueError:
		utils.die("unable to determine insert size")

	# Load in the histogram, which has a bin per insert size.
	histogram = dict(enumerate(map(int, open(histfile).readlines())))
	database.store(_run_id, "histogram", histogram)


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
		self.lookup("insert", "insert_size.estimate_insert.bowtie2")
		self.retrieve("histogram")
		# Generators
		self.generator(self.insert_table)
		if self.outdir:
			self.generator(self.insert_histogram)

	def insert_table(self):
		return self.summarize(report.insert_schema, "insert")

	def insert_histogram(self):
		"""A histogram of insert sizes."""
		if self.check("histogram"):
			# Generate a histogram that is rebinned to 20 insert sizes
			# per bin.
			imgname = "%d.insert.hist.png" % self.run_id
			props = {
				"title": "Distribution of Insert Sizes",
				"xlabel": "Insert Size (bp)",
				"ylabel": "Frequency"}
			return [self.histogram(imgname, self.data.histogram, props=props)]

# vim: noexpandtab ts=4 sw=4
