#!/usr/bin/env python

"""Function that reads one or more yaml makefiles and checks them"""


import re
import copy
import glob
import string
import os
import os.path

from inputlib import \
    check_lib, \
    InputLibraryError

from paleomix.common.console import \
    print_warn, \
    print_err

from paleomix.common.makefile import \
    MakefileError,   \
    read_makefile,   \
    IsBoolean,       \
    IsNone,          \
    IsInt,           \
    IsStr,           \
    StringStartsWith,\
    ValueIn,         \
    ValueGE,         \
    ValuesSubsetOf,  \
    IsDictOf,        \
    IsListOf,        \
    And,             \
    Or,              \
    Not,             \
    REQUIRED_VALUE


def read_makefiles(filenames, config):
    """metaBIT makefiles reader"""
    makefiles = []
    for filename in filenames:
        # Check structure and apply defaults (if has default value)
        # where no value specified
        makefile = read_makefile(filename, _VALIDATION)
        # Check that values are valid (path, programs, libraries)
        makefiles.append(_check_update(makefile, config))
    return makefiles


def _alphanum_check(whitelist):
    description = "characters a-z, A-Z, 0-9%s allowed"
    description %= (", and %r" % whitelist,) if whitelist else ""

    whitelist += string.ascii_letters + string.digits

    return And(IsStr(), ValuesSubsetOf(whitelist, description=description))


_VALID_NAME = And(_alphanum_check("._-"),
                  ValueGE(2, key=len,
                          description="at least two characters long"))

_VALID_GROUP_NAME = And(_VALID_NAME, StringStartsWith('G_'))
_VALID_SAMPLE_NAME = And(_VALID_NAME, Not(StringStartsWith('G_')))

_VALID_LIB_NAME = And(_alphanum_check("._-\\&"),
                      ValueGE(2, key=len,
                              description="at least two characters long"))

_TRIMMED_TYPES = set(("Collapsed", "Paired", "Singles"))

_IS_LANE = IsDictOf(ValueIn(_TRIMMED_TYPES),
                    Or(IsStr, IsListOf(IsStr)))

_IS_SAMPLE = {
    _VALID_SAMPLE_NAME: {
        _VALID_LIB_NAME: Or(IsStr, _IS_LANE, default=REQUIRED_VALUE)
    }
}

_IS_SAMPLE[_VALID_GROUP_NAME] = _IS_SAMPLE


_OPT_VALUE = Or(IsListOf(IsBoolean, IsInt, IsStr),
                Or(IsNone, IsBoolean, IsInt, IsStr))
_OPTIONS = { StringStartsWith("-"): _OPT_VALUE }

# REQUIRED:     root:Samples:Libname:path
#           and root:Bowtie2:References
# The rest has defaults
_VALIDATION = {
        'OutDir':  IsStr,
        'keepfromPE': {
            'Collapsed': IsBoolean(default=True), # includes CollapsedTruncated
            'Paired': IsBoolean(default=True),
            'Singles': IsBoolean(default=True)
            },
        # Allow for *optional* extra levels of grouping, above the sample level
        'Samples': _IS_SAMPLE,
        'Bowtie2': {
            '--no-discordant': IsBoolean(default=True),
            StringStartsWith('-'): _OPT_VALUE
            },
        'Metaphlan': {
            'Exclude': Or(IsStr, IsListOf(IsStr), default=[]),
            'Pool': Or(IsStr, IsListOf(IsStr), default=[]),
            StringStartsWith('-'): _OPT_VALUE
            },
        'run_from_table': IsStr,
        'Statax': {'rename_taxlevels': IsDictOf(
                                            ValueIn(('k','p','c','o','f','g','s','t')),
                                            IsStr),

                   # One subdictionary per run (useful when applying different options)
                   IsStr: {
                      'merge': IsListOf(IsStr),
                      'taxlevels': Or(IsStr, IsListOf(IsStr), default='pcofgs'),
                      'filterout': IsInt(default=1),
                      ValueIn(('doDiv','doBarplot','doHeatmap',
                          'doPcoa','doClust')): _OPTIONS
                          }
                 },
        'Krona': {'run': IsBoolean(default=True),
                  'no_underscore': IsBoolean(default=True),
                  '-a': IsBoolean(default=True), # graph visible without internet.
                  StringStartsWith("-"): _OPT_VALUE
                 },
        'Lefse': {'run': IsBoolean(default=False),
                  'merge': IsListOf(IsStr),
                  'outdir': IsStr(default='lefse'),
                  'format': ValueIn(("png", "pdf", "svg"), default="pdf"),
                  'Groups': IsDictOf(IsStr,
                                     Or(IsListOf(IsStr),
                                        IsDictOf(IsStr, IsListOf(IsStr)))),
                  'format_input': {"-o": IsInt(default=1000000),
                                   StringStartsWith("-"): _OPT_VALUE
                                  },
                  'run_lefse':      _OPTIONS,
                  'plot_res':       _OPTIONS,
                  'plot_cladogram': _OPTIONS,
                  'plot_features':  _OPTIONS
                  }
        }


def _update_outdir(makefile, config, filename):
    outdir = makefile.get('OutDir',
                          "out_" + os.path.splitext(os.path.basename(filename))[0])
    outdir = config.destination or outdir
    outdir = os.path.split(outdir.rstrip('/'))
    if not outdir[0]:
        outdir = os.path.join(*outdir)
    else:
        if not os.path.isdir(outdir[0]):
            raise MakefileError(("The leading path to output directory is not"
                                 " an existing directory:\n%s") % outdir[0])
        else:
            outdir = os.path.join(*outdir)

    makefile['OutDir'] = outdir


def _get_lefse_groups(samples, key=None, sep='_'):
    """Recursive function.
    It gets the tree of nested groups of samples,
    while in the same time flattening the dictionary named 'samples'.
    Since this structure might not be the most practical for the user,
    the groups for the LEfSe can also be given as a list in the Lefse:Groups field"""

    subsamples = samples.get(key, samples)
    if all(key.startswith('G_') for key in subsamples):
        groups = {}
        for key in subsamples:
            groups[key.replace('G_', '')] = _get_lefse_groups(subsamples, key)
            subsamples.update(subsamples.pop(key))
    else:
        groups = []
        for key, subsub in subsamples.iteritems(): #subsub is supposed to be a lib
            # join sample _ lib with an underscore
            groups += [key + sep + subkey for subkey in sorted(subsub)]

    return groups


def _check_lefse_groups(makefile, grouplist, sep = "_"):
    wrong = []
    for group_item in grouplist:
        sample_lib = group_item.split(sep)
        if sample_lib[0] not in makefile['Samples'] or \
          (len(sample_lib)>1 and sample_lib[1] not in makefile['Samples'][sample_lib[0]]):
            wrong.append("Group absent from samples: %s" % group_item)

    return "\n".join(wrong) + "\n" if wrong else ""


def _update_lefse_groups(makefile):
    lefse_groups = _get_lefse_groups(makefile['Samples'])

    if not makefile['Lefse'].get('Groups'):
        makefile['Lefse']['Groups'] = lefse_groups
    elif isinstance(lefse_groups, dict):
        raise MakefileError(("You cannot give Lefse groups in the 'Lefse:Groups' "
                             "entry and in the 'Samples' entry."))
    else:
        pass
        # check that the groups correspond to the samples and libs
        # error_msg = ''
        # for G_key, G_val in makefile['Lefse']['Groups'].iteritems():
        #     if isinstance(G_val, dict):
        #         for subG_key, subG_val in G_val.iteritems():
        #             error_msg += _check_lefse_groups(makefile, subG_val)
        #     else:
        #         error_msg += _check_lefse_groups(makefile, G_val)
        # if error_msg:
        #     raise MakefileError("Wrong Lefse groups:\n" + error_msg)



def _update_libs(makefile):
    """goes into libpath, find the files and characterizes the lib as PE or
    SE"""

    # check that files are not included multiple times
    file_set = set()
    for Samplename in makefile['Samples']:
        for Libname in makefile['Samples'][Samplename]:
            Lib = makefile['Samples'][Samplename].pop(Libname)

            if isinstance(Lib, str): # i.e a folder is given.
                if '\\' in Libname:
                    # check if user is already listing content of directory using '*'
                    Lib = Lib.rstrip('/')
                    if '*' in os.path.basename(Lib) or \
                       '*' in os.path.dirname(Lib):
                        # append '/' to get only directories
                        Lib = Lib + '/'
                    # if no wildcard, you MUST add it for glob to list content or directory
                    else:
                        raise MakefileError("If you specify several libraries, "
                                            "please use wildcards '*' in path.\n"
                                            "Wrong path: %s\nSuggestion: %s" %( \
                                                    Lib, Lib + '/*/'))

                    Lib_list = glob.glob(Lib)
                    regex = Lib.replace('*', '(.*)')
                    regex = re.compile(regex)

                    if Libname == '\\&':
                        Libname_list = ['_'.join(regex.search(elem).groups()) \
                                        for elem in Lib_list]
                    else:
                        # then Libname contains \1 or \2, etc, so use it as a pattern:
                        # replace \1 by first match or '*', \2 by second, etc.
                        Libname_list = [regex.sub(Libname, elem) for elem in Lib_list]

                    nb_lib_found = 0
                    for (newname, new) in zip(Libname_list, Lib_list):
                        try:
                            inputlib = check_lib(new)

                            if "Collapsed" in inputlib or \
                                  "Paired" in inputlib:
                                for trimmed_type in inputlib:
                                    if not makefile['keepfromPE'][trimmed_type]:
                                        inputlib.pop(trimmed_type)
                            makefile['Samples'][Samplename][newname] = inputlib

                            nb_lib_found += 1

                        except InputLibraryError as e:
                            print_warn(e)

                    if not nb_lib_found:
                        raise MakefileError("The given path does not contain "
                                "any library:\n%s" %Lib + "\n"
                                "Expected files (default output of AdapterRemoval):\n"
                                "SE: *.truncated           [.gz|.bz2]\n"
                                "PE: *.collapsed           [.gz|.bz2]\n"
                                "    *.collapsed.truncated [.gz|.bz2]\n"
                                "    *.pair1.truncated     [.gz|.bz2]\n"
                                "    *.pair2.truncated     [.gz|.bz2]\n"
                                "    *.singleton.truncated [.gz|.bz2]\n"
                                "If other names are used, please specify it "
                                "explicitly in the yaml using the following "
                                "structure:\n"
                                "Libname:\n"
                                "  Collapsed: path/to/collapsed\n"
                                "  Paired: path/to/pair{Pair}\n"
                                "  Singles: path/to/singleton\n"
                                "# use 'Singles' key for SE libraries\n")
                else:
                    inputlib = check_lib(Lib)

                    if "Collapsed" in inputlib or "Paired" in inputlib:
                        for trimmed_type in inputlib:
                            if not makefile['keepfromPE'][trimmed_type]:
                                inputlib.pop(trimmed_type)

                    makefile['Samples'][Samplename][Libname] = inputlib

            elif isinstance(Lib, dict):
                if set(Lib) <= _TRIMMED_TYPES:
                    newlib = {}
                    for trimmed_type, values in Lib.iteritems():
                        files = []
                        if isinstance(values, str):
                            values = [values]
                        for f in values:
                            if trimmed_type == 'Paired':
                                files += zip(sorted(glob.glob(f.format(Pair=1))),
                                             sorted(glob.glob(f.format(Pair=2))))
                            else:
                                files += [(x, None) for x in glob.glob(f)]

                        newlib[trimmed_type] = files

                    makefile['Samples'][Samplename][Libname] = newlib

        for libname, lib in makefile['Samples'][Samplename].items():
            for trimtype, file_list in lib.iteritems():
                try:
                    file_list, _ = zip(*file_list)
                except ValueError as e:
                    raise MakefileError("File not found for sample: %s %s %s" % (\
                                                        Samplename, libname, trimtype))
                if file_set.isdisjoint(file_list):
                    file_set |= set(file_list)
                else:
                    same_files = " ".join(file_set.intersection(file_list))
                    print_err("Identical files specified in 2 different libraries:\n"
                              "%s\n"
                              "Library %s will be ignored.\n" %(same_files,
                                                                libname))
                    makefile['Samples'][Samplename].pop(libname)
                    break


def _update_pools(makefile):
    """Reformat the 'Exclude' and 'Pool' content of the makefile"""
    excl = makefile["Metaphlan"].pop("Exclude")
    if isinstance(excl, str):
        excl = [excl]
    for Sample_Lib in excl:
        Sample, Lib = Sample_Lib.split(":")
        if Sample not in makefile['Samples']:
            raise MakefileError("The specified sample '%s' to exclude does "
                                "not exist in your input samples: %s"
                                % (Sample,
                                   " ".join(makefile['Samples'])))
        elif Lib not in makefile['Samples'][Sample]:
            raise MakefileError("In sample '%s': the specified library '%s' to"
                                " exclude does not exist in your sample: %s"
                                % (Sample, Lib,
                                   " ".join(makefile['Samples'][Sample])))
    makefile["Metaphlan"]["Exclude"] = excl

    pools = makefile["Metaphlan"].pop("Pool")
    if isinstance(pools, str):
        if pools == '*':
            pools = makefile['Samples'].keys()
        else:
            pools = [pools]

    for pool in pools:
        if pool not in makefile['Samples']:
            raise MakefileError("The specified sample '%s' to pool does not "
                                "exist in your input samples: %s"
                                % (pool, " ".join(makefile['Samples'])))

    makefile["Metaphlan"]["Pool"] = pools


def _update_statax(makefile):
    default_taxlevels = {'k': 'Kingdoms',
                         'p': 'Phyla',
                         'c': 'Classes',
                         'o': 'Orders',
                         'f': 'Families',
                         'g': 'Genera',
                         's': 'Species',
                         't': 'Strains'}
    rename_taxlevels = makefile['Statax'].get('rename_taxlevels', {})
    default_taxlevels.update(rename_taxlevels)
    makefile['Statax']['rename_taxlevels'] = default_taxlevels


def _update_metaphlan_options(makefile, config):
    """Applies metaphlan2 options if required"""
    metaphlan_script = os.path.join(config.metaphlan_path, "metaphlan2.py")
    if metaphlan_script.endswith("metaphlan2.py"):
        makefile['Metaphlan']['--mpa_pkl'] \
            = os.path.join(config.metaphlan_path,
                           "db_v20/mpa_v20_m200.pkl")
        # Required for merge_table:
        makefile['Metaphlan']['--sample_id_key'] = 'ID'


def _check_update(makefile, config):
    """Check values in makefile (path, file) and """
    makefile = copy.deepcopy(makefile)
    filename = makefile["Statistics"]["Filename"]
    makefile = makefile.pop("Makefile")

    _update_outdir(makefile, config, filename)
    if not makefile.get('run_from_table'):
        if makefile['Lefse']['run']:
            _update_lefse_groups(makefile)
        _update_libs(makefile)
        _update_pools(makefile)
        _update_metaphlan_options(makefile, config)

    _update_statax(makefile)
    return makefile
