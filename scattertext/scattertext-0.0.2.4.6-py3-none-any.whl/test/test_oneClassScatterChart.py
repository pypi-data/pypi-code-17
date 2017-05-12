from unittest import TestCase

from scattertext.OneClassScatterChart import OneClassScatterChart
from scattertext.test.test_termDocMatrixFactory \
	import build_hamlet_jz_term_doc_mat


class TestOneClassScatterChart(TestCase):
	def test_main(self):
		tdm = build_hamlet_jz_term_doc_mat()
		scatterchart = OneClassScatterChart(tdm)
