#!/usr/bin/env python

import re
import os
import os.path
from glob import glob
from itertools import izip_longest

from paleomix.common.makefile import MakefileError
from paleomix.common.console  import print_info


_trimmed_types = ['Collapsed', 'Pair1', 'Pair2', 'Singles']

# This is AdapterRemoval default output (see man AdapterRemoval).
# If using Paleomix bam_pipeline, the files are gzipped/bzipped
_reg_PE = {'Collapsed': re.compile(r'^.*\.collapsed(\.truncated|)(\.gz|\.bz2|)$'),
           'Pair1':     re.compile(r'.*\.pair1\.truncated\.(gz|bz2)$'),
           'Pair2':     re.compile(r'.*\.pair2\.truncated\.(gz|bz2)$'),
           'Singles':   re.compile(r'.*\.singleton\.truncated\.(gz|bz2)$')}
_reg_SE = re.compile(r'.*\.truncated\.(gz|bz2)$')


class InputLibraryError(MakefileError):
    """Raised if library does not meet requirements
    (wrong path, wrong files, etc)"""


def _fmt_info(path, files):
    files_1, files_2 = zip(*files) or ([], [])
    if any(files_2):
        files_1 = [f.replace("pair1", "pair[12]") for f in files_1]
    files = [f.replace(path+"/", "") for f in files_1]
    return ("\n" + " "*16).join(files)


def check_lib(path):
    """Automatically find trimmed reads files in 'path'"""
    if not os.path.isdir(path):
        raise InputLibraryError("The specified library path is not a "
                                "regular existing directory:\n%s" %path)
    path = os.path.abspath(path)
    files = os.listdir(path)
    lib = {k: [] for k in ('Collapsed', 'Paired', 'Singles')}
    
    isPE = False

    for root, dirs, files in os.walk(path):
        tmp = {}
        for k in _trimmed_types:
            tmp[k] = [os.path.join(root, f) for f in files if _reg_PE[k].match(f)]

        if not any(tmp.values()):
            lib['Singles'] += [(os.path.join(root, f), None) for f in files if _reg_SE.match(f)]

        else:
            lib['Collapsed'] += [(x, None) for x in tmp['Collapsed']]
            lib['Singles']   += [(x, None) for x in tmp['Singles']]
            lib['Paired']    += zip(tmp['Pair1'], tmp['Pair2'])
            isPE |= True

    print_info("\nAuto-detect files in library folder:  %s" % path)

    if not isPE and len(lib['Singles']) > 0 :
        lib.pop('Collapsed')
        lib.pop('Paired')
    elif not isPE:
        raise InputLibraryError("  Found no pre-trimmed fastq files (expected "
                                "file names:\n  default output of "
                                "AdapterRemoval/Paleomix)\n")

    print_info("  %s detected." % (isPE*"PE" or "SE",))
    for k,v in lib.iteritems():
            print_info("  - {:<11} {}".format(k + " :", _fmt_info(path, v)))
    
    return lib
