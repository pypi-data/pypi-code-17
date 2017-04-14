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

import codecs
import os
import textwrap

from collections import defaultdict, OrderedDict
from docutils.core import publish_parts
from string import Template

from biolite import catalog
from biolite import diagnostics
from biolite import report
from biolite import utils

from agalma import config
from agalma import qc
from agalma import insert_size
from agalma import rrna
from agalma import assemble
from agalma import translate
from agalma import homologize
from agalma import multalign
from agalma import genetree
from agalma import treeinform
from agalma import treeprune
from agalma import supermatrix
from agalma import speciestree
from agalma import expression

def profile_pipeline(run_id):
	values = diagnostics.lookup(
				run_id, "%s.%s" % (diagnostics.INIT, diagnostics.RUSAGE))
	start = float(values['timestamp'])
	values = diagnostics.lookup(
				run_id, "%s.%s" % (diagnostics.EXIT, diagnostics.RUSAGE))
	values['walltime'] = float(values['timestamp']) - start
	profile = list()
	for field in report.rusage_schema:
		try:
			profile.append("%-19s: %12s" % (
				field.title,
				field.format.format(field.type(values[field.key]))))
		except KeyError:
			profile.append("%-19s: %12s" % (field.title, '-'))
	return '\n'.join(profile)

def catalog_header(record):
	row = "<tr><td><b>%s</b></td><td>%s</td></tr>"
	html = [
		'<blockquote>',
		'<table class="table table-striped table-condensed">',
		row % (catalog.fields[0], record[0])]
	html += [row % x for x in zip(catalog.fields[3:-1], record[3:-1]) if x[1]]
	html.append("</table>\n</blockquote>")
	return html

def report_runs(id, outdir, run_ids=None, verbose=False, show_hidden=False, bootstrap_css=None):
	outdir = os.path.abspath(outdir)
	utils.safe_mkdir(outdir)

	if not id and run_ids is None:
		utils.die("must specify a catalog id or a list of run ids")

	if id:
		record = catalog.select(id)
		if record is None:
			utils.info("no catalog entry found for id '%s'" % id)
			record = catalog.make_record(id=id)
		title = record.species if record.species else id
	else:
		title = "Agalma runs %s" % ','.join(run_ids)

	if bootstrap_css is None:
		bootstrap_css = 'css/bootstrap.min.css'
		report.copy_css(outdir)

	html = ["""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>%s</title>
<link href="%s" rel="stylesheet" media="screen">
<style type="text/css">
body {
  margin: 30px 50px;
}
.stats {
  margin: 10px;
  display: none;
}
.table {
  font-size: 14px;
  font-family: Monaco,Menlo,Consolas,"Courier New",monospace;
}
.table-mini {
  width: 50%%;
}
div.stage { padding: 10px 0 10px 0; border-top: 5px solid #eee; }
blockquote p { font-size: 14px; }
.btn-lg,
.btn-group-lg > .btn {
  padding: 10px 16px;
  font-size: 18px;
  line-height: 1.33;
  border-radius: 6px;
}
</style>
<script type="text/javascript">
function togglestats(element){
	element.nextElementSibling.style.display == "none" || element.nextElementSibling.style.display == "" ?
		element.nextElementSibling.style.display = "table" :
		element.nextElementSibling.style.display = "none";
}
</script>
%%SCRIPT%%
</style>
</head>
<body>
<h1><em>%s</em></h1>""" % (title, bootstrap_css, title)]

	if id:
		html += catalog_header(record)

	js = []
	toc = []
	content = defaultdict(list)
	sections = (
		qc,
		insert_size,
		rrna,
		assemble,
		translate,
		homologize,
		multalign,
		genetree,
		treeprune,
		supermatrix,
		speciestree,
		expression)

	if run_ids:
		runs = map(diagnostics.lookup_run, run_ids)
	else:
		runs = diagnostics.lookup_runs(id)

	for run in runs:
		if not run.done:
			utils.info("skipping unfinished run %d" % run.id)
			continue
		elif (not show_hidden) and run.hidden > 0:
			utils.info("skipping hidden run %d" % run.id)
			continue
		links = list()
		# Try to generate a report for each section and add it to the content.
		pipelines = diagnostics.lookup_pipelines(run.id)
		utils.info(run.id, "has pipelines:", ','.join(pipelines))
		for section in sections:
			name = section.__name__.partition('.')[2]
			if name in pipelines:
				run_report = section.Report(id, run.id, outdir, hlevel=4, verbose=verbose)
				if run_report:
					utils.info("added", name, "report for", run.id)
					links.append("<li><a href=\"#{0}_{1}\">{0}</a></li>".format(name, run.id))
					desc = publish_parts(
								textwrap.dedent(section.__doc__),
								writer_name='html')
					content[run.id] += [
"""<div id="{0}_{1}" class="stage">
<h2>{0} <small>(Run {1})</small></h2>
<blockquote>
{2}
</blockquote>""".format(name, run.id, desc['body']),
						str(run_report),
						'<a class="btn" href="#toc"><i class="icon-list"></i> Back to TOC</a>',
						'</div>']
					js += run_report.get_js()
		# Print a header with basic information about the run.
				else:
					utils.info("warning:", name, "report failed for", run.id)
		toc.append("""
			<tr class="minimal">
				<td class="minimal">
				<b>Run %s</b><br/><i>%s</i><br/>%s<br/>%s
				</td>
				<td class="minimal">
				<ul>%s</ul>
				</td>
				<td class="minimal">
				<pre>%s</pre>
				</td>
			</tr>""" % (
				run.id, run.name, run.timestamp, run.hostname,
				''.join(links), profile_pipeline(run.id)))

	merged_js = OrderedDict()
	for include in js:
		merged_js[include] = None
	html[0] = html[0].replace('%SCRIPT%', '\n'.join(merged_js))
	html.append('<h2 id="toc">Table of Contents</a></h2><table class="table table-striped">')
	html += toc
	html.append("</table>")
	for run_id in sorted(content):
		if content[run_id]:
			html += content[run_id]
	html.append("</body></html>")

	# Final output.
	with codecs.open(os.path.join(outdir, 'index.html'), 'w', 'utf-8') as f:
		f.write('\n'.join(line.replace('\t','') for line in html if line))

# vim: noexpandtab sw=4 ts=4
