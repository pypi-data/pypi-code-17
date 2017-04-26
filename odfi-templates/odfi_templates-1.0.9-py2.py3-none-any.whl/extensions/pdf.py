import sys
import os
import glob
from os.path import basename
from os.path import dirname
import posixpath
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.compat import make_admonition
from sphinx.locale import _


from sphinx.util import logging
import logging


from xml.etree import ElementTree

from sphinx.builders import Builder



class Pdf(nodes.Inline, nodes.Element):
	"""PDF Node"""



def visit_pdf_node(self, node):
	print("Visit pdf: ",self.builder,"\n")
	
	finalPath = posixpath.join(self.builder.dlpath,node.fileName)
	self.builder.env.dlfiles[node.file] = [node.file,node.fileName]
	#self.builder.images[node.file]= "lecture"
	self.body.append('<canvas class="pdfjs" data-file="%s">' %(finalPath))


def depart_pdf_node(self, node):
	self.body.append('</canvas>')




class OdfiPdfDirective(Directive):
	has_content = True
	optional_arguments = 1
	def run(self):

		pdfNode = Pdf()

		## Get File, relative to current source
		###############

		fileName = self.arguments[0]
		env = self.state.document.settings.env
		source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
		sourceDirectory = dirname(source)
		pdfFile  = os.path.normpath(sourceDirectory+"/"+fileName)

		## Normalize name because of upper case issues on windows
		pdfFile = "%s[%s]" % (pdfFile[:-1], pdfFile[-1])
		pdfFile = glob.glob(pdfFile)[0]

		if os.path.exists(pdfFile):
			print("PDF File is at: ",pdfFile)
		else:
			return [nodes.error(None, nodes.paragraph(text = "Unable to Load PDF File at %s:%d: file %s does not exist" % (basename(source), self.lineno,pdfFile))) ]


		pdfNode.fileName  = fileName
		pdfNode.file = pdfFile

		## Set content
		pdfNode.content = self.content

		return [pdfNode]




def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_node(Pdf, html=(visit_pdf_node, depart_pdf_node))
	app.add_directive('odfi.pdf',OdfiPdfDirective)



	return {'version': '1.0.0'}