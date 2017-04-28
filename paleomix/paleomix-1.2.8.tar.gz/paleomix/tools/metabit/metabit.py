#!/usr/bin/env python
import sys
import time
import logging
import os.path
import subprocess

import paleomix
import paleomix.yaml
import paleomix.logger
from paleomix.pipeline import Pypeline
from paleomix.common.console import print_err, print_info

import parts
from makefile import MakefileError, read_makefiles
from config import parse_config


_tools = {"filterMetaphlan":  ["nodes", "tools", "filterMetaphlan.py"],
          "get_stats":        ["nodes", "tools", "get_stats.py"],
          "metaphlan2krona":  ["nodes", "tools", "metaphlan2krona_2.py"],
          "reformat_taxa":    ["nodes", "tools", "reformat_taxa.py"],
          "doPcoa":           ["nodes", "tools", "statax_Rmodule", "doPcoa.R"],
          "doClust":          ["nodes", "tools", "statax_Rmodule", "doClust.R"],
          "doDiv":            ["nodes", "tools", "statax_Rmodule", "doDiv.R"],
          "doHeatmap":        ["nodes", "tools", "statax_Rmodule", "doHeatmap.R"]}


def run(config, args):
    logfile_template = time.strftime("metaBIT.%Y%m%d_%H%M%S_%%02i.log")
    paleomix.logger.initialize(config, logfile_template)
    logger = logging.getLogger(__name__)
    try:
        logger.info("Building metaBIT pipeline ...")
        makefiles = read_makefiles(args, config)
    except (MakefileError, paleomix.yaml.YAMLError, IOError), error:
        print_err("Error reading makefiles:",
                  "\n  %s:\n   " % (error.__class__.__name__,),
                  "\n    ".join(str(error).split("\n")),
                  file=sys.stderr)
        return 1

    # setups for the logfile
    pipeline = Pypeline(config=config)

    for makefile in makefiles:
        if not makefile.get('run_from_table'):
            rmdup_nodes, metaphlan_nodes, summary_node \
                = parts.profiling(makefile, config)

            pipeline.add_nodes(rmdup_nodes, summary_node)
            pipeline.add_nodes(parts.analyzing(makefile, config, metaphlan_nodes))
        else:
            pipeline.add_nodes(parts.analyzing(makefile, config))

    if config.list_output_files:
        logger.info("Printing output files ...")
        pipeline.print_output_files()
        return 0
    elif config.list_executables:
        logger.info("Printing required executables ...")
        pipeline.print_required_executables()
        return 0

    logger.info("MetaBIT running now!")
    if not pipeline.run(dry_run=config.dry_run,
                        max_threads=config.max_threads,
                        progress_ui=config.progress_ui):
        return 1

    return 0


def _print_usage():
    print_info("METAGENOMICS Pipeline %s\n"
               % (paleomix.__version__,))
    print_info("Usage:")
    print_info("  paleomix metabit makefile.yaml")


def main(argv):
    if argv and argv[0] in _tools:
        path = os.path.dirname(os.path.realpath(__file__))
        command = os.path.join(*[path] + _tools[argv[0]])
        return subprocess.call([command] + argv[1:])

    config, args = parse_config(argv)
    if not args:
        _print_usage()
        print_err("\nPlease specify at least one makefile!\n")
        return 1

    return run(config, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
