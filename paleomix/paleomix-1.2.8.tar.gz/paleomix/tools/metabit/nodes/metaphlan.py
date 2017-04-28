#!/usr/bin/env python

import pysam
import os.path

from itertools import izip, izip_longest
import paleomix.common.fileutils as fileutils

from paleomix.common.utilities import safe_coerce_to_tuple
from paleomix.node import Node, CommandNode, NodeError
from paleomix.atomiccmd.builder import AtomicCmdBuilder, \
                                       create_customizable_cli_parameters, \
                                       use_customizable_cli_parameters

from tools.reformat_taxa import merge_tables

_tmp_inputfile = "tmp_bowtie2out.tsv"


class MetaphlanNode(CommandNode):
    @create_customizable_cli_parameters
    def customize(cls, metaphlan, input_files, output_file, threads=1,
                  dependencies=[], ID = ''):

        input_files = safe_coerce_to_tuple(input_files)
        input_files = list(input_files)
        
        call = [metaphlan,
                "--nproc", threads,
                "--input_type", "bowtie2out",
                "%(TEMP_OUT_FILE)s", "%(OUT_FILE)s"]
        
        cmd = AtomicCmdBuilder(call,
                               TEMP_OUT_FILE = _tmp_inputfile,
                               OUT_FILE = output_file)
        
        cmd.set_kwargs(**{"IN_FILE_%02i" %(i+1,): infile \
                                    for i,infile in enumerate(input_files)})
        
        return {"command": cmd}


    @use_customizable_cli_parameters
    def __init__(self, parameters):
        
        self.output_file = parameters.output_file
        
        if not parameters.ID:
            self.ID = os.path.dirname( \
                            parameters.output_file).replace("/", "_") or \
                      os.path.splitext(parameters.output_file)[0]
        else:
            self.ID = parameters.ID

        basenames = [os.path.basename(f) for f in parameters.input_files]
        
        desc = "<MetaPhlan: %r: %s -> %r>" %(self.ID,
                                            "\n".join(parameters.input_files), 
                                            parameters.output_file)
        CommandNode.__init__(self, parameters.command.finalize(),
                            description=desc,
                            threads=parameters.threads,
                            dependencies=parameters.dependencies)


    def _setup(self, _config, _temp):
        """Create a temporary file of the bowtie2out format from the input
        BAMs (merge if several):
        bowtie2out is the format returned by metaphlan when only running
        bowtie2. These are the 1st and 3d columns of the SAM returned by
        bowtie2 (QNAME and RNAME). Format required when using
        'metaphlan --input_type bowtie2out' """
        CommandNode._setup(self, _config, _temp)

        # Additional step: create the temporary "bowtie2out" file
        input_files = list(self.input_files)
        output_file = os.path.join(_temp, _tmp_inputfile)
        
        with open(output_file, 'w') as OUT_BOWTIE:
            for infile in input_files:
                with pysam.AlignmentFile(infile, 'rb') as IN_BAM:
                    references = IN_BAM.references
                    for read in IN_BAM:
                        OUT_BOWTIE.write("%s\t%s\n" %(read.query_name,
                                                      references[read.tid]))

        CommandNode._check_for_missing_files(self, output_file, "Temporary input file")


class MergeTablesNode(Node):
    def __init__(self, output_file, samplefiles, dependencies = (), **merge_opts):
        self.samplefiles = samplefiles
        self.output_file = output_file
        self.merge_opts = merge_opts

        input_files = [value[0] for value in samplefiles]

        desc = "<merge metaphlan tables: %s -> %r>" %(("\n"+" "*25).join(input_files),
                                                      os.path.basename(output_file))

        Node.__init__(self,
                      input_files = input_files,
                      output_files = output_file,
                      description = desc,
                      dependencies = dependencies)

    def _run(self, _config, _temp):
        output_file, = self.output_files
        output_file = os.path.join(_temp, os.path.basename(output_file))
        merge_tables(output_file, self.samplefiles, **self.merge_opts)

    def _teardown(self, _config, _temp):
        expected_files = [os.path.join(_temp, os.path.basename(f)) for f in \
                                                       list(self.output_files)]
        self._check_for_missing_files(expected_files, "output")
        for tmp_f, commited_f in zip(expected_files, list(self.output_files)):
            fileutils.move_file(tmp_f, commited_f)


class Metaphlan2LefseNode(Node):
    def __init__(self, input_file, output_file, sep='_', groups=None, dependencies=()):
        self.sep = sep
        if groups:
            self.groups = groups
        else:
            raise NodeError("No groups given to the LEfSe input, the LEfSe "
                            "cannot be run.")

        desc = "<Specify groups of samples in the merged metaphlan table>"
        Node.__init__(self, input_files = input_file,
                            output_files = output_file,
                            description = desc,
                            dependencies = dependencies)
    
    def _run(self, _config, _temp):

        input_file, = self.input_files
        output_file, = self.output_files
        output_file = os.path.join(_temp, os.path.basename(output_file))
        
        with open(input_file) as IN:
            ID_line = IN.readline()
            IDs = ID_line.rstrip().split("\t")
            # Warning: the user should preferably not use underscores in sample names
            #sample_names = [ID.split(self.sep)[0] for ID in IDs]

            order = [0] #the first column is for the row names
            allgroups = []
            for groups, samples in iterate_tree(self.groups):
                for s in samples:
                    try:
                        allgroups.append(groups)
                        order.append(IDs.index(s))
                    except ValueError as e: # when sample name not in the IDs
                        raise NodeError(e.message + \
                                "\nList of sample names: %s" % " ".join(IDs))

            with open(output_file, 'w') as OUT:
                grouplevel = "class"
                for groupline in izip_longest(*allgroups, fillvalue=''):
                    OUT.write(grouplevel + "\t" + "\t".join(groupline) + "\n")
                    grouplevel = "sub" + grouplevel

                OUT.write("\t".join(IDs[i] for i in order) + "\n")

                for line in IN:
                    line = line.rstrip().split("\t")
                    OUT.write("\t".join(line[i] for i in order) + "\n")


    def _teardown(self, _config, _temp):
        expected_files = [os.path.join(_temp, os.path.basename(f)) for f in \
                                                                list(self.output_files)]
        self._check_for_missing_files(expected_files, "output")
        for tmp_f, commited_f in zip(expected_files, list(self.output_files)):
            fileutils.move_file(tmp_f, commited_f)


def iterate_tree(tree, path=()):
    """tree is a nested dictionary. This function creates an iterator
    yielding the deepest elements of the tree with the corresponding path"""
    if isinstance(tree, dict):
        for key, value in tree.iteritems():
            for elem in iterate_tree(value, path + (key,)):
                yield elem
    else:
        yield path, tree
