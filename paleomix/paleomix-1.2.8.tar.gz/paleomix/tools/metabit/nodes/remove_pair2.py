#!/usr/bin/env python

""" 
    Filter mapped paired-end data:
    if the two pairs mapped to the same reference, remove one of them,
    in order to avoid counting twice when estimating taxon abundance.
"""

import os.path
import pysam

from paleomix.node import Node


class removePair2Node(Node):
    def __init__(self, input_file, output_file, output_file_trash, dependencies=()):
        """'dependency' should be the bowtie2Node"""
        
        self.outsam = output_file
        self.outtrash = output_file_trash

        description = "< Remove pair2 %s -> %s >" \
                      % (os.path.basename(input_file),
                         os.path.basename(output_file))

        Node.__init__(self,
                      description  = description,
                      input_files  = input_file,
                      output_files = [output_file, output_file_trash],
                      dependencies = dependencies)
    
    def _run(self, config, temp):
        input_file, = self.input_files

        processed_qnames = []
        
        with pysam.AlignmentFile(input_file, 'r') as IN_SAM:
            with pysam.AlignmentFile(self.outsam, 'wh', template=IN_SAM) as OUT_SAM: 
                with pysam.AlignmentFile(self.outtrash, 'wh', template=IN_SAM) as OUT_TRASH: 
                    for read in IN_SAM:
                        if read.query_name not in processed_qnames :
                            processed_qnames.append(read.query_name)
                            OUT_SAM.write(read)
                        else:
                            OUT_TRASH.write(read)

