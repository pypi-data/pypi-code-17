#!/usr/bin/env python

""" For each library, builds the nodes corresponding to the sequence of:
    - Bowtie2,
    - picardtools SortSam,
    - bam_rmdup / MarkDuplicates,
    - Samtools view (to remove marked duplicates)
    - Metaphlan.
"""

import os.path
import nodes.tools as tools

from paleomix.common.console import \
    print_warn

from paleomix.common.fileutils import \
    swap_ext

from paleomix.atomiccmd.builder import \
    apply_options

from paleomix.nodes.bowtie2 import \
    Bowtie2Node
from nodes.remove_pair2 import \
    removePair2Node
from paleomix.nodes.picard import \
    MarkDuplicatesNode
from paleomix.nodes.commands import \
    FilterCollapsedBAMNode
from nodes.metaphlan import \
    MetaphlanNode, \
    MergeTablesNode, \
    Metaphlan2LefseNode

# for krona, statax, lefse:
from nodes.execute import \
    ExecNode, \
    SimpleExecNode, \
    ExecModuleNode


_trimmed_types = ("Collapsed", "Paired", "Singles")


def profiling(makefile, config, sep='_'):
    """returns nodes from the profiling, ready to be used by the Rscripts part
    sep is the string separating sample name and library name in the output"""
    rmdup_nodes_list = []
    metaphlan_nodes_list = []
    summary_params = {'dependencies': [],
                      'input_files': [],
                      'IDs': [],
                      'directories': [],
                      'function_in_args': None,
                      'function_out_args': ['output_file'],
                      'output_file': os.path.join(makefile['OutDir'],
                                                  'summary_readcounts.tsv')}
    summary_params['output_files'] = summary_params['output_file']

    for (Samplename, Sample) in makefile['Samples'].iteritems():
        metaphlan_params = []

        for (Libname, inputlib) in Sample.iteritems():
            folder = os.path.join(makefile['OutDir'], Samplename, Libname)
            ID = Samplename + sep + Libname
            summary_params['directories'].append(folder)
            summary_params['IDs'].append(ID)

            if Samplename not in makefile['Metaphlan']['Pool']:
                output_file = os.path.join(folder, 'taxa.tsv')
                metaphlan_params.append({"dependencies": [],
                                         "input_files": [],
                                         "output_file": output_file,
                                         "ID": ID})

            elif not metaphlan_params:
                print_warn("Pooling sample: " + Samplename)

                folder = os.path.join(makefile['OutDir'], Samplename)

                output_file = os.path.join(folder, 'taxa.tsv')
                metaphlan_params.append({"dependencies": [],
                                         "input_files": [],
                                         "output_file": output_file,
                                         "ID": Samplename})

            for trimmed_type, input_files in inputlib.iteritems():
                dependencies = ()
                output_name = 'reads.' + trimmed_type.lower()
                input_files_1, input_files_2 = zip(*input_files)
                bowtie2_options = makefile['Bowtie2']

                if not all(input_files_2):
                    if any(input_files_2):
                        # There cannot be a different number of pair1 and pair2
                        raise BaseException
                    else:
                        input_files_2 = None
                else:
                    bowtie2_options.update({PEopt: True for PEopt in
                                           ['--no-discordant']})
                                            #'--no-overlap']})

                output_base = os.path.join(makefile['OutDir'],
                                           Samplename, Libname,
                                           output_name + '.bowtie2out')
                output_file = output_base + '.bam'
                log_file = output_base + '.stats'

                # Bowtie2
                alignment_node = _build_bowtie2_nodes(config=config,
                                                      input_files_1=input_files_1,
                                                      input_files_2=input_files_2,
                                                      output_file=output_file,
                                                      log_file=log_file,
                                                      dependencies=dependencies,
                                                      options=makefile['Bowtie2'])
                summary_params['input_files'].append(log_file)
                summary_params['dependencies'].append(alignment_node)

                if trimmed_type == 'Paired':
                    input_file = output_file
                    output_file = swap_ext(input_file, 'mate1.bam')
                    output_file_trash = swap_ext(input_file, 'mate2.bam')
                    remove_pair2_node = removePair2Node(input_file,
                                                        output_file,
                                                        output_file_trash,
                                                        dependencies=alignment_node)
                    dependencies = (remove_pair2_node,)
                else:
                    dependencies = (alignment_node,)

                # Remove duplicates
                input_file = output_file
                output_file = input_file.replace('.bam', '.filtered.bam')

                rmdup_cls = FilterCollapsedBAMNode if trimmed_type == 'Collapsed' \
                            else MarkDuplicatesNode
                rmdup_node = rmdup_cls(config       = config,
                                       input_bams    = (input_file,),
                                       output_bam   = output_file,
                                       keep_dupes   = False,
                                       dependencies = dependencies)
                summary_params['input_files'].append(output_file)
                summary_params['dependencies'].append(rmdup_node)

                if Samplename+":"+Libname in makefile['Metaphlan']['Exclude']:
                    print_warn("Excluding  %s:%s (%s)" % (Samplename, Libname,
                                                          trimmed_type))
                    rmdup_nodes_list.append(rmdup_node)
                else:
                    metaphlan_params[-1]['input_files'].append(output_file)
                    metaphlan_params[-1]['dependencies'].append(rmdup_node)
                # END of for-loop on each trimmed_type
            # END of the for-loop on each library
        #still in the for-loop on each sample:
        for params in metaphlan_params:
            metaphlan_nodes_list.append(_build_metaphlan_node(config, params,
                                                       makefile['Metaphlan']))

    summary_node = ExecModuleNode('nodes.tools.get_stats',
                                  'gather_stats',
                                  description = 'Summarize read counts',
                                  **summary_params)

    return rmdup_nodes_list, metaphlan_nodes_list, summary_node


def analyzing(makefile, config, metaphlan_nodes=(), group='all'):
    nodes = []
    statax_dep = ()
    runonly = makefile.get('run_from_table')

    if metaphlan_nodes:
        statax_in = os.path.join(makefile['OutDir'], group+'_taxa.tsv')
        merge_in = [[node.output_file, node.ID] for node in metaphlan_nodes]
        merge_samples_node = MergeTablesNode(output_file = statax_in,
                                             samplefiles = merge_in,
                                             dependencies = metaphlan_nodes,
                                             idstr = 'ID',
                                             keep_original_IDs = False)
        nodes.append(merge_samples_node)
        statax_dep += (merge_samples_node,)

    elif not runonly:
        # Metaphlan nodes are expected if statax is not set in runonly mode
        raise RuntimeError
    else:
        statax_in = runonly

    rename_taxlevels = makefile['Statax'].pop('rename_taxlevels')

    statax_path = os.path.join(os.path.abspath(tools.__path__[0]),
                               "statax_Rmodule")

    # list of list of files for merging (one list per merge)
    merge_list = []
    # one per different merging
    filter_nodes = []

    for run_name, run in makefile['Statax'].iteritems():
        run_outdir = os.path.join(makefile['OutDir'], 'statax', run_name)

        merge = run.get("merge")
        if merge not in merge_list:
            merge_list.append(merge)
            if merge:
                filter_infile = os.path.join(run_outdir, run_name + '.tsv')
                samplefiles = [[f] for f in [statax_in] + merge]
                merge_node = MergeTablesNode(
                                output_file = filter_infile,
                                samplefiles = samplefiles,
                                dependencies = statax_dep)
                                #keep_original_IDs = False)
                filter_dep = merge_node
            else:
                filter_infile = statax_in
                filter_dep = statax_dep

            filter_outbase = os.path.join(run_outdir, 'tables', run_name)
            filter_taxlevels = 'kpcogfst' if makefile['Metaphlan'].get('--mpa_pkl') \
                                          else 'kpcofgs'
            filter_outfiles = [filter_outbase + '_filtered_' + L + '.tsv' for L in \
                                                                       filter_taxlevels]
            filter_outfiles += [filter_outbase + '_filtered_samples.txt',
                                filter_outbase + '_filtered_taxa_sum.tsv',
                                filter_outbase + '_filtered_taxa_nb.tsv']
            filter_node = ExecModuleNode("nodes.tools.filterMetaphlan",
                                         "dofilter",
                                         input_files=filter_infile,
                                         output_files=filter_outfiles,
                                         dependencies = filter_dep,
                                         function_in_args=["inputfile"],
                                         function_out_args=None,
                                         function_out_tmp="outbase",
                                         outbase = filter_outbase,
                                         filterout = run['filterout'],
                                         taxlevels=filter_taxlevels)

            filter_nodes.append(filter_node)
            nodes.append(filter_node)
            run_dep = filter_node

            doDiv = run.get('doDiv')
            if doDiv is not None:
                div_node = SimpleExecNode(os.path.join(statax_path, 'doDiv.R'),
                                          description = '%s: doDiv' % run_name,
                                          input_file = filter_infile,
                                          output_file=os.path.join(run_outdir,
                                              run_name + "_diversities.tsv"),
                                          options=doDiv,
                                          dependencies = filter_dep)
                nodes.append(div_node)

        else: # merge in merge_list
            i = merge_list.index(merge)
            run_dep = filter_nodes[i]

        for L in run['taxlevels']:
            longL = rename_taxlevels[L]
            for operation in ['doBarplot', 'doHeatmap', 'doPcoa', 'doClust']:
                op = run.get(operation)
                if op is not None:
                    call = [os.path.join(statax_path, operation+".R"),
                            "%(IN_FILE)s"]
                    builder_kwargs = {'IN_FILE':
                            run_dep.function_kwargs['outbase'] + '_filtered_' + L + '.tsv'}
                    op_node = ExecNode.customize(call,
                                description="%s: %s (%s)" %(run_name, operation, longL),
                                threads=op.get('--ncores', 1),
                                dependencies=run_dep,
                                builder_kwargs=builder_kwargs)
                    out_base = os.path.join(run_outdir, run_name + '_' + \
                                operation.replace('do','').lower() + \
                                '_' + longL)
                    if operation in ['doBarplot', 'doHeatmap']:
                        op_node.command.add_value("%(OUT_PDF)s")
                        op_node.command.set_kwargs(OUT_PDF = out_base+'.pdf')
                        op_node.command.set_option('--title',
                            "%s abundances (level: %s)" %(run_name, longL))
                        op_node.command.set_option('--taxon_title', longL)
                    else:
                        op_node.command.set_option('--pdf', "%(OUT_PDF)s")
                        op_node.command.set_option('--tsv', "%(OUT_TSV)s")
                        op_node.command.set_kwargs(OUT_PDF= out_base + '.pdf',
                                                   OUT_TSV= out_base + '.tsv')
                        if operation == 'doClust':
                            op_node.command.set_option('--RData', "%(OUT_RDATA)s")
                            op_node.command.set_kwargs(OUT_RDATA=out_base+'.RData')

                    apply_options(op_node.command, op)
                    nodes.append(op_node.build_node())

    # Krona
    if makefile['Krona']['run'] and not runonly:
        output_base = os.path.join(makefile['OutDir'], 'krona')
        krona_input_files = []
        krona_dep = []
        for node in metaphlan_nodes:
            krona_infile = os.path.join(output_base, node.ID + ".krona.in")
            convert_node = ExecModuleNode("nodes.tools.metaphlan2krona_2",
                                          "convert",
                                          input_files = node.output_file,
                                          output_files = krona_infile,
                                          dependencies = node,
                                          description="convert metaphlan out -> krona in",
                                          function_in_args = ["inputfile"],
                                          function_out_args = ["outputfile"],
                                          no_underscore=True)

            krona_input_files.append(krona_infile)
            krona_dep.append(convert_node)

        output_file = os.path.join(output_base, group + '_taxa.krona.html')
        krona_node = ExecNode.customize(("ktImportText", '-o', "%(OUT_FILE)s"),
                               description="<krona: ktImportText -> %s>" % output_file,
                               dependencies = krona_dep,
                               builder_kwargs={"OUT_FILE": output_file})
        krona_node.command.set_option("-a", True, fixed=False)
        apply_options(krona_node.command, makefile['Krona'])
        krona_node.command.add_multiple_values(krona_input_files)

        nodes.append(krona_node.build_node())

    # LEfSe
    if makefile['Lefse']['run']:

        if makefile['Lefse'].get('merge'):
            input_file = os.path.join(makefile['OutDir'], makefile['Lefse']['outdir'],
                        os.path.basename(statax_in).replace('.tsv', '_merged.tsv'))
            samplefiles = [[f] for f in [statax_in] + makefile['Lefse']['merge']]
            lefse_merge_node = MergeTablesNode(output_file = input_file,
                                         samplefiles = samplefiles,
                                         dependencies = statax_dep)
                                         #keep_original_IDs = False)
            statax_dep = lefse_merge_node
        else:
            input_file = statax_in

        # format input by including groups on top of the sample names
        pre_lefse_input = os.path.join(makefile['OutDir'], makefile['Lefse']['outdir'],
                        os.path.basename(input_file).replace('.tsv', '.lefse.in.tsv'))

        metaphlan2lefse_node = Metaphlan2LefseNode(input_file = input_file,
                                                   output_file = pre_lefse_input,
                                                   groups = makefile['Lefse']['Groups'],
                                                   dependencies = statax_dep)

        run_lefse_input = pre_lefse_input.replace('lefse.in.tsv', 'lefse.in')

        subclass_nb = max((len(path) for path,_ in \
                                          _iterate_tree(makefile['Lefse']['Groups'])))
        format_options={"-c": 1,
                        "-s": 2 if subclass_nb==2 else -1,
                        "-u": 3 if subclass_nb==2 else 2}
        format_options.update(makefile["Lefse"]["format_input"])

        format_input_node = SimpleExecNode(os.path.join(config.lefse_path,
                                                        "format_input.py"),
                                           pre_lefse_input,
                                           run_lefse_input,
                                           options = format_options,
                                           dependencies = metaphlan2lefse_node)

        run_lefse_output = run_lefse_input.replace('lefse.in', 'lefse.out')
        run_lefse_node = SimpleExecNode(os.path.join(config.lefse_path, "run_lefse.py"),
                                  run_lefse_input,
                                  run_lefse_output,
                                  makefile["Lefse"]["run_lefse"],
                                  dependencies = format_input_node)

        fmt = makefile['Lefse']['format']
        for step in ['plot_res', 'plot_cladogram', 'plot_features']:
            if not makefile['Lefse'][step].has_key('--format'):
                makefile['Lefse'][step]['--format'] = fmt

        plot_res_node = SimpleExecNode(os.path.join(config.lefse_path, "plot_res.py"),
                                  run_lefse_output,
                                  run_lefse_output.replace('lefse.out', 'lefse.plot_res.'+fmt),
                                  makefile["Lefse"]["plot_res"],
                                  dependencies = run_lefse_node)
        plot_clad_node = SimpleExecNode(os.path.join(config.lefse_path, "plot_cladogram.py"),
                                  run_lefse_output,
                                  run_lefse_output.replace('lefse.out','lefse.cladogram.'+fmt),
                                  makefile["Lefse"]["plot_cladogram"],
                                  dependencies = run_lefse_node)

        plot_features_obj = ExecNode.customize(os.path.join(config.lefse_path,
                                                            "plot_features.py"),
                                               #description="Lefse: plot_features",
                                               dependencies = (metaphlan2lefse_node,
                                                           run_lefse_node))
        plot_features_obj.command.add_value(run_lefse_input) # dataset file
        plot_features_obj.command.add_value(run_lefse_output)
        plot_features_obj.command.add_value(run_lefse_output.replace('out', 'biomarkers.zip')) # output file
        plot_features_obj.command.set_option("--archive", "zip")
        apply_options(plot_features_obj.command, makefile['Lefse']['plot_features'])

        plot_features_node = plot_features_obj.build_node()

        nodes.extend([run_lefse_node,plot_clad_node,plot_res_node,plot_features_node])

    return nodes


def _build_bowtie2_nodes(config, input_files_1, input_files_2, output_file,
                         log_file, dependencies, options):

    prefix = os.path.join(config.metaphlan_path, "db_v20", "mpa_v20_m200")
    params = Bowtie2Node.customize(input_file_1=input_files_1,
                                   input_file_2=input_files_2,
                                   output_file=output_file,
                                   reference=None,
                                   prefix=prefix,
                                   log_file=log_file,
                                   threads=config.bowtie2_max_threads,
                                   dependencies=dependencies)

    apply_options(params.commands['aln'], {"--no-unal": True})
    apply_options(params.commands['aln'], options)

    return params.build_node()


def _build_metaphlan_node(config, params, options):
    if not params['output_file']:
        raise RuntimeError("No input given to metaphlan, you made a mistake somewhere.\n"
                           "have you excluded all the libraries of sample %s ?" %Samplename)
    else:
        metaphlan_script = os.path.join(config.metaphlan_path, "metaphlan2.py")
        node = MetaphlanNode.customize(metaphlan_script,
                                       threads=config.metaphlan_max_threads,
                                       **params)
        apply_options(node.command, options)
    return node.build_node()


def _iterate_tree(tree, path=()):
    """Iterate over a tree of nested dictionary, flattening the output:
    each most inside value is returned with the set of keys leading to it (path)"""
    if isinstance(tree, dict):
        for key, value in tree.iteritems():
            for elem in _iterate_tree(value, path+(key,)):
                yield elem
    else:
        yield path, tree

