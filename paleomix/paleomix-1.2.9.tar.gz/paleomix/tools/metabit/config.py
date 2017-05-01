#!/usr/bin/env python


"""Parse arguments from command line and return a tuple (config, args)"""

#from glob import glob
#import os.path
import optparse

import paleomix
import paleomix.ui

from paleomix.config import PerHostConfig, PerHostValue, ConfigError


__foreword__ = """
metaBIT, an integrative and automated metagenomic pipeline for analysing
microbial profiles from high-throughput sequencing shotgun data

Guillaume Louvel, Clio Der Sarkissian, Ludovic Orlando.
Centre for GeoGenetics, Natural History Museum of Denmark, University of Copenhagen.
Version: %s
                              -----
""" % paleomix.__version__


__description__ = """%prog processes trimmed reads produced using shotgun
high through-put DNA sequencing, provided in fastq (or compressed gz/bz2), and
generates taxonomic microbial profiles as well as their statistical comparison
across samples, libraries, environments, etc."""


__epilog__ = """Please report bugs and suggestions for improvements to:
Guillaume Louvel (guillaume.louvel@ens.fr)
Clio Der Sarkissian (clio.dersarkissian@snm.ku.dk)
Kristian hanghoej (k.hanghoej@snm.ku.dk)
Ludovic Orlando (lorlando@snm.ku.dk)
"""


class metaBITHelpFormatter(optparse.IndentedHelpFormatter):
    def format_usage(self, usage):
        return usage + "\n"

    def format_epilog(self, epilog):
        return "\n" + epilog


def _run_config_parser(argv):
    # Helper class for optparse.OptionParser
    # allows reading from and writing to a config file
    per_host_cfg = PerHostConfig("metaBIT")

    usage_str    = ("Usage:\n  %prog [options] makefile.yaml  # yaml formatted file, "
                    "other extensions allowed\n"
                    "  %prog [options] --write-config # configure metaBIT "
                    "dependencies for future runs")
    version_str  = "%%prog %s" % (paleomix.__version__,)


    parser       = optparse.OptionParser(usage = __foreword__ + "\n" + usage_str,
                                         version = version_str,
                                         description = __description__,
                                         epilog = __epilog__,
                                         formatter=metaBITHelpFormatter(),
                                         prog="metaBIT")
    
    paleomix.ui.add_optiongroup(parser,
                                ui_default=PerHostValue("quiet"),
                                color_default=PerHostValue("on"))
    paleomix.logger.add_optiongroup(parser, default = PerHostValue("warning"))

    group  = optparse.OptionGroup(parser, "Scheduling")
    group.add_option("--bowtie2-max-threads", type = int, default = PerHostValue(2),
                     help = "Maximum number of threads to use per Bowtie 2 "
                     "instance [%default]")
    group.add_option("--metaphlan-max-threads", type = int, default = PerHostValue(2),
                     help = "Maximum number of threads to use per MetaPhlAn "
                     "instance [%default]")
    group.add_option("--max-threads", type = int, default = per_host_cfg.max_threads,
                     help = "Maximum number of threads to use in total [%default]")
    group.add_option("--dry-run", action = "store_true", default = False,
                     help = "If passed, only a dry-run in performed, the dependency "
                     "tree is printed, and no tasks are executed.")
    parser.add_option_group(group)

    group  = optparse.OptionGroup(parser, "Required paths")
    group.add_option("--jar-root", default = PerHostValue("~/install/jar_root",
                                                          is_path = True),
                     help = "Folder containing Picard JARs (http://picard.sf.net) " \
                     "[%default]")
    group.add_option("--temp-root", default = per_host_cfg.temp_root,
                     help = "Location for temporary files and folders [%default/]")
    group.add_option("--destination", default = None,
                     help = "The destination folder for result files. By default, "
                     "files will be placed in ./out_{makefile name}/")
    group.add_option("--metaphlan-path", default = PerHostValue("~/install/metaphlan",
                                                                is_path=True),
                     help = "Path to the folder containing metaphlan(2).py and " \
                     "the database [%default]")
    group.add_option("--lefse-path", default = PerHostValue("~/install/lefse",
                                                            is_path = True),
                     help = "Path to the LEfSe executables [%default] "
                     "(https://bitbucket.org/nsegata/lefse, "
                     "\"Metagenomic biomarker discovery and explanation\", "
                     "Segata et al. 2011)")
    parser.add_option_group(group)

    group  = optparse.OptionGroup(parser, "Misc")
    group.add_option("--jre-option", dest = "jre_options", action = "append",
                     default = PerHostValue([]),
                     help = "May be specified one or more times with options to be "
                            "passed to the JRE (Jave Runtime Environment); e.g. to "
                            "change the maximum amount of dedicated RAM (default is %default)")
    parser.add_option_group(group)

    group  = optparse.OptionGroup(parser, "Files and executables")
    group.add_option("--list-output-files", action = "store_true", default = False,
                     help = "List all files generated by metaBIT for a given makefile")
    group.add_option("--list-orphan-files", action = "store_true", default = False,
                     help = "List all files at destination not generated by the pipeline. " \
                            "This option is useful for rerunning metaBIT after editing the makefile from a previous analysis. If the same destination is required and the same name is given for the" 
                       " set of analyses, metaBIT will NOT erase the results of previous analyses,"
                       " even if new parameters are required. It will then report the list of such "
                       "files for traceability. Useful only for cleaning up after making changes "
                       "to a makefile.")
    group.add_option("--list-executables", action="store_true", default=False,
                     help="List all executables required by the pipeline, "
                          "with version requirements (if any).")
    parser.add_option_group(group)

    return per_host_cfg.parse_args(parser, argv)


def parse_config(argv):
    config, args = _run_config_parser(argv)
    paleomix.ui.set_ui_colors(config.ui_colors)

#    FIXME: Nuke?
#    if not glob( os.path.join(config.metaphlan_path, "metaphlan*.py")):
#        raise ConfigError(("Wrong metaphlan-path: %s\n'metaphlan*.py' not found"))

    if config.list_output_files and config.list_orphan_files:
        raise ConfigError("Error: Both --list-output-files and --list-orphan-files set!")

    return config, args
