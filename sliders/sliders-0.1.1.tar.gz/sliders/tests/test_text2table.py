#!/usr/bin/env python

import unittest

from sliders import text2table

class TestText2Table(unittest.TestCase):
    
    def test_single_input(self):
        inputs=[
                './text2table.py',
                '--schema=fastqc', 
                '../tests/sample_fastqc.data']
        text2table.Text2Table(inputs)

    def test_single_input_out(self):
        inputs=[
                './text2table.py',
                '--schema=fastqc',
                '--output-file=../tests/test_fastqc.csv', 
                '../tests/sample_fastqc.data']
        text2table.Text2Table(inputs)

    def test_multiple_input_files(self):
        inputs=[
                './text2table.py', 
                '--schema=fastqc',
                '../tests/sample_fastqc.data',
                '../tests/sample_fastqc_2.data']
        text2table.Text2Table(inputs)

    def test_multiple_input_files_static(self):
        inputs=[
                './text2table.py', 
                '--schema=fastqc',
                '--static-values=series=test,sample=A',
                '../tests/sample_fastqc.data',
                '../tests/sample_fastqc_2.data']
        text2table.Text2Table(inputs)

    def test_static_out(self):
        inputs=[
                './text2table.py',
                '--schema=fastqc',
                '--static-values=series=test,sample=A',
                '--output-file=../tests/test_static_fastqc.csv', 
                '../tests/sample_fastqc.data']
        text2table.Text2Table(inputs)

if __name__ == '__main__':
    unittest.main()