#!/usr/bin/env python

import os.path
import pysam

from paleomix.node import Node, CommandNode, NodeError
from paleomix.atomiccmd.command import AtomicCmd
from paleomix.atomiccmd.sets import \
     ParallelCmds
from paleomix.atomiccmd.builder import \
     AtomicCmdBuilder

import paleomix.common.versions as versions


_COMMON_CHECK = versions.GE(1, 1, 0)

SAMTOOLS_VERSION = versions.Requirement(
    call=("samtools", "--version"),
    search=r"samtools (\d+)\.(\d+)\.?(\d+)?",
    checks=_COMMON_CHECK)



class SortSamNode(CommandNode):
    """sorts SAM file and returns a BAM"""

    def __init__(self, input_file, output_file, dependencies=()):
        cmd_sam2bam = AtomicCmd(["samtools", "view", "-buS", "%(IN_SAM)s"],
                                IN_SAM = input_file,
                                OUT_STDOUT = AtomicCmd.PIPE,
                                CHECK_VERSION = SAMTOOLS_VERSION)
        cmd_sortbam = AtomicCmd(["samtools", "sort",
                                 "-T", "%(TEMP_OUT_PREFIX)s",
                                 "-o", "%(OUT_BAM)s",
                                 "-O", "bam",
                                 "-"],
                                IN_STDIN=cmd_sam2bam,
                                # when starting with TEMP_OUT, temp_root path
                                # is added automatically
                                TEMP_OUT_PREFIX="SamToBam",
                                OUT_BAM=output_file)

        description = "< samtools: view (sam to bam) and sort\n %s -> %s >" \
                      % (os.path.basename(input_file),
                         os.path.basename(output_file))

        CommandNode.__init__(self,
                             command      = ParallelCmds([cmd_sam2bam,
                                                          cmd_sortbam]),
                             description  = description,
                             #threads      = parameters.threads,
                             dependencies = dependencies)


class SortSamNode2(Node):
    """sort using pysam"""
    def __init__(self, input_file, output_file, dependencies=()):
        description = "< pysam sort (sam to bam)\n %s -> %s >" \
                      % (os.path.basename(input_file),
                         os.path.basename(output_file))
        Node.__init__(self,
                      description, 
                      input_files=input_file,
                      output_files=output_file,
                      dependencies=dependencies)
    
    def _run(self, config, temp):
        input_file, = self.input_files
        output_file, = self.output_files
        with pysam.AlignmentFile(input_file, 'r') as IN_SAM:
            reads = [read for read in IN_SAM]
            reads.sort(key=lambda read: read.rname)

            with pysam.AlignmentFile(output_file, 'wb', template=IN_BAM) as OUT_BAM:
                for read in reads:
                    OUT_BAM.write(read)


### Not used. This conversion is done in the _setup step of the MetaphlanNode.
class BAM2bowtie2outNode(Node):
    def __init__(self, input_file, output_file, dependencies=()):
        """'dependency' should be the rmdup_node"""

        description = "< Format SAM to bowtie2out format\n %s -> %s >" \
                      % (os.path.basename(input_file),
                         os.path.basename(output_file))

        Node.__init__(self,
                      description  = description,
                      #threads      = parameters.threads,
                      input_files  = input_file,
                      output_files = output_file,
                      #requirement  =
                      dependencies = dependencies)
    
    def _run(self, config, temp):
        input_file,  = self.input_files
        output_file, = self.output_files
        with open(output_file, 'w') as OUT_BOWTIE:
            with pysam.AlignmentFile(input_file, 'rb') as IN_BAM:
                references = IN_BAM.references
                for read in IN_BAM:
                    OUT_BOWTIE.write("%s\t%s\n" %(read.query_name,
                                                  references[read.tid]))


#class BAMIndexNode(CommandNode):
#    """Index a BAM file using 'samtools index'."""
#
#    def __init__(self, infile, dependencies=()):
#        cmd_index = AtomicCmd(["samtools", "index", "%(IN_BAM)s",
#                               "%(OUT_BAI)s"],
#                              IN_BAM=infile,
#                              OUT_BAI=swap_ext(infile, ".bai"),
#                              CHECK_SAM=SAMTOOLS_VERSION)
#
#        CommandNode.__init__(self,
#                             description="<BAMIndex: '%s'>" % (infile,),
#                             command=cmd_index,
#                             dependencies=dependencies)

