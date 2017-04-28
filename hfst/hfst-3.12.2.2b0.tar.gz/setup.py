#!/usr/bin/python3

"""
Setup for creating PIP packages for HFST Python bindings.

Before running setup, recursively copy directories 'libhfst/src'
and 'back-ends' from HFST c++ source code under the directory where
setup is run (on linux and os x with copy-files.sh and on windows with
copy-files-win.sh). Make sure that the following c++ and header files 
from 'libhfst/src/parsers' have been generated from flex/yacc files
before copying (on linux and os x by running 'make' and on windows
with 'compile-parsers-win.sh' located in 'libhfst/src/parsers'):

  lexc-lexer.cc pmatch_lex.cc xfst-lexer.cc xre_lex.cc sfst-scanner.cc
  lexc-parser.cc pmatch_parse.cc xfst-parser.cc xre_parse.cc sfst-compiler.cc
  lexc-parser.hh pmatch_parse.hh xfst-parser.hh xre_parse.hh sfst-compiler.hh

Compiling the extensions requires python, swig and a c++ compiler, 
all located on a directory listed on system PATH. On linux and mac 
osx, readline and getline must be available and the c++ compiler
must support flag 'std=c++11'.

The setup script has been tested on linux with gcc 4.6.3, swig 3.0.12 and
python 3.4 and on windows with swig 3.0.5 and msvc 10.0 (with python 3.3.
and 3.4) and msvc 14.0 (with python 3.5 and 3.6).

"""

from setuptools import setup, Extension

from sys import platform
if platform == "darwin":
    import os
    os.environ["_PYTHON_HOST_PLATFORM"] = 'macosx-10.7-x86_64'

def readme():
    with open('README.rst') as f:
        return f.read()

# HFST C++ headers needed by swig when creating the python/c++ interface
swig_include_dir = "libhfst/src/"

ext_swig_opts = ["-c++", "-I" + swig_include_dir, "-Wall"]
import sys
# for python3.3 and python3.4 on windows, add SDK include directory
if platform == "win32" and sys.version_info[0] == 3 and (sys.version_info[1] == 3 or sys.version_info[1] == 4):
    ext_swig_opts.extend(["-IC:\\Program Files (x86)\\Microsoft SDKs\\Windows\\v7.0A\\Include"])

# readline is needed for hfst.start_xfst(), on windows the shell where HFST
# python bindings are run from has its own readline which will do
ext_extra_link_args = []
if platform == "linux" or platform == "linux2" or platform == "darwin":
    ext_extra_link_args = ['-lreadline']
if platform == "darwin":
    ext_extra_link_args.extend(['-mmacosx-version-min=10.7'])

# HFST headers needed when compiling the actual c++ extension
ext_include_dirs = [".", "libhfst/src/", "back-ends/foma", "back-ends",
                    "parsers", "libhfst/src/parsers"]
if platform == "win32":
    ext_include_dirs.append("back-ends/openfstwin/src/include")
else:
    ext_include_dirs.append("back-ends/openfst/src/include")

# this replaces ./configure
ext_define_macros = [ ('HAVE_OPENFST', None), ('HAVE_OPENFST_LOG', None) ]

# at the moment, foma back-end is disabled on os x as
# clang doesn't accept "-std=c++11" or "-std=c++0x" flag when compiling C
if platform == "linux" or platform == "linux2" or platform == "win32":
    ext_define_macros.append(('HAVE_FOMA', None))
if platform == "linux" or platform == "linux2" or platform == "darwin":
    ext_define_macros.append(('HAVE_READLINE', None))
    ext_define_macros.append(('HAVE_GETLINE', None))
if platform == "win32":
    # MSC_VER_ should already be defined
    for macro in ["HFSTEXPORT", "OPENFSTEXPORT", "WINDOWS", "WIN32", "_CRT_SECURE_NO_WARNINGS"]:
        ext_define_macros.append((macro, None))

# use c++0x standard, if possible
ext_extra_compile_args = []
if platform == "linux" or platform == "linux2" or platform == "darwin":
    ext_extra_compile_args = ["-std=c++0x", "-Wno-sign-compare", "-Wno-strict-prototypes"]
if platform == "darwin":
    ext_extra_compile_args.extend(["-stdlib=libc++", "-mmacosx-version-min=10.7"])
# define error handling mechanism on windows
if platform == "win32":
    ext_extra_compile_args = ["/EHsc"]

ext_library_dirs = []
ext_libraries = []

# on windows, c++ source files have 'cpp' extension
cpp = ".cc"
if platform == "win32":
    cpp = ".cpp"

# on windows, openfst back-end is in directory 'openfstwin'
openfstdir = "openfst"
if platform == "win32":
    openfstdir = "openfstwin"

# all c++ extension source files
libhfst_source_files = ["libhfst/src/parsers/XfstCompiler" + cpp,
                        "libhfst/src/HfstApply" + cpp,
                        "libhfst/src/HfstInputStream" + cpp,
                        "libhfst/src/HfstTransducer" + cpp,
                        "libhfst/src/HfstOutputStream" + cpp,
                        "libhfst/src/HfstRules" + cpp,
                        "libhfst/src/HfstXeroxRules" + cpp,
                        "libhfst/src/HfstDataTypes" + cpp,
                        "libhfst/src/HfstSymbolDefs" + cpp,
                        "libhfst/src/HfstTokenizer" + cpp,
                        "libhfst/src/HfstFlagDiacritics" + cpp,
                        "libhfst/src/HfstExceptionDefs" + cpp,
                        "libhfst/src/HarmonizeUnknownAndIdentitySymbols" + cpp,
                        "libhfst/src/HfstLookupFlagDiacritics" + cpp,
                        "libhfst/src/HfstEpsilonHandler" + cpp,
                        "libhfst/src/HfstStrings2FstTokenizer" + cpp,
                        "libhfst/src/HfstPrintDot" + cpp,
                        "libhfst/src/HfstPrintPCKimmo" + cpp,
                        "libhfst/src/hfst-string-conversions" + cpp,
                        "libhfst/src/string-utils" + cpp,
                        "libhfst/src/implementations/HfstBasicTransducer" + cpp,
                        "libhfst/src/implementations/HfstBasicTransition" + cpp,
                        "libhfst/src/implementations/ConvertTransducerFormat" + cpp,
                        "libhfst/src/implementations/HfstTropicalTransducerTransitionData" + cpp,
                        "libhfst/src/implementations/ConvertTropicalWeightTransducer" + cpp,
                        "libhfst/src/implementations/ConvertLogWeightTransducer" + cpp,
                        "libhfst/src/implementations/ConvertFomaTransducer" + cpp,
                        "libhfst/src/implementations/ConvertOlTransducer" + cpp,
                        "libhfst/src/implementations/TropicalWeightTransducer" + cpp,
                        "libhfst/src/implementations/LogWeightTransducer" + cpp,
                        "libhfst/src/implementations/FomaTransducer" + cpp,
                        "libhfst/src/implementations/HfstOlTransducer" + cpp,
                        "libhfst/src/implementations/compose_intersect/ComposeIntersectRulePair" + cpp,
                        "libhfst/src/implementations/compose_intersect/ComposeIntersectLexicon" + cpp,
                        "libhfst/src/implementations/compose_intersect/ComposeIntersectRule" + cpp,
                        "libhfst/src/implementations/compose_intersect/ComposeIntersectFst" + cpp,
                        "libhfst/src/implementations/compose_intersect/ComposeIntersectUtilities" + cpp,
                        "libhfst/src/implementations/optimized-lookup/transducer" + cpp,
                        "libhfst/src/implementations/optimized-lookup/convert" + cpp,
                        "libhfst/src/implementations/optimized-lookup/ospell" + cpp,
                        "libhfst/src/implementations/optimized-lookup/pmatch" + cpp,
                        "libhfst/src/implementations/optimized-lookup/find_epsilon_loops" + cpp,
                        "libhfst/src/parsers/xre_lex" + cpp,
                        "libhfst/src/parsers/xre_parse" + cpp,
                        "libhfst/src/parsers/pmatch_parse" + cpp,
                        "libhfst/src/parsers/pmatch_lex" + cpp,
                        "libhfst/src/parsers/lexc-parser" + cpp,
                        "libhfst/src/parsers/lexc-lexer" + cpp,
                        "libhfst/src/parsers/xfst-parser" + cpp,
                        "libhfst/src/parsers/xfst-lexer" + cpp,
                        "libhfst/src/parsers/LexcCompiler" + cpp,
                        "libhfst/src/parsers/PmatchCompiler" + cpp,
                        "libhfst/src/parsers/XreCompiler" + cpp,
                        "libhfst/src/parsers/lexc-utils" + cpp,
                        "libhfst/src/parsers/pmatch_utils" + cpp,
                        "libhfst/src/parsers/xre_utils" + cpp,
                        "libhfst/src/parsers/xfst-utils" + cpp,
                        "libhfst/src/parsers/xfst_help_message" + cpp,
                        "libhfst/src/parsers/sfst-scanner" + cpp,
                        "libhfst/src/parsers/sfst-compiler" + cpp,
                        "libhfst/src/parsers/SfstCompiler" + cpp,
                        "libhfst/src/parsers/SfstAlphabet" + cpp,
                        "libhfst/src/parsers/SfstBasic" + cpp,
                        "libhfst/src/parsers/SfstUtf8" + cpp ]

foma_source_files = [ "back-ends/foma/int_stack.c",
                      "back-ends/foma/define.c",
                      "back-ends/foma/determinize.c",
                      "back-ends/foma/apply.c",
                      "back-ends/foma/rewrite.c",
                      "back-ends/foma/topsort.c",
                      "back-ends/foma/flags.c",
                      "back-ends/foma/minimize.c",
                      "back-ends/foma/reverse.c",
                      "back-ends/foma/extract.c",
                      "back-ends/foma/sigma.c",
                      "back-ends/foma/structures.c",
                      "back-ends/foma/constructions.c",
                      "back-ends/foma/coaccessible.c",
                      "back-ends/foma/io.c",
                      "back-ends/foma/utf8.c",
                      "back-ends/foma/spelling.c",
                      "back-ends/foma/dynarray.c",
                      "back-ends/foma/mem.c",
                      "back-ends/foma/stringhash.c",
                      "back-ends/foma/trie.c",
                      "back-ends/foma/lex.yy.c",
                      "back-ends/foma/regex.c" ]

openfst_source_files =  [ "back-ends/" + openfstdir + "/src/lib/compat" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/flags" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/fst" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/properties" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/symbol-table" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/symbol-table-ops" + cpp,
                          "back-ends/" + openfstdir + "/src/lib/util" + cpp ]

libhfst_source_files = libhfst_source_files + openfst_source_files

# At the moment, foma back-end is disabled on os x. See the following comment.
if platform == "linux" or platform == "linux2" or platform == "win32":
    libhfst_source_files = libhfst_source_files + foma_source_files

# clang doesn't accept "-std=c++11" flag when compiling C,
# so foma back-end must be compiled separately
# it seems that subprocess doesn't work, so you must compile them manually before running setup.py:
# for file in back-ends/foma/*.c; do clang -fPIC -std=c99 -arch i386 -arch x86_64 -mmacosx-version-min=10.7 -DHAVE_FOMA -c $file ; done
foma_object_files = []
#if platform == "darwin":
#    for file in foma_source_files:
#        foma_object_files.append(file.replace('back-ends/foma/','').replace('.c','.o'))

# The HFST c++ extension
libhfst_module = Extension('_libhfst',
                           language = "c++",
                           sources = ["libhfst.i"] + libhfst_source_files,
                           swig_opts = ext_swig_opts,
                           include_dirs = ext_include_dirs,
                           library_dirs = ext_library_dirs,
                           libraries = ext_libraries,
                           define_macros = ext_define_macros,
                           extra_link_args = ext_extra_link_args,
                           extra_compile_args = ext_extra_compile_args,
                           extra_objects = foma_object_files
                           )

setup(name = 'hfst',
      version = '3.12.2.2_beta',
      author = 'HFST team',
      author_email = 'hfst-bugs@helsinki.fi',
      url = 'http://hfst.github.io/',
      description = 'Python interface for HFST',
      long_description = readme(),
      license = 'GNU GPL3',
      ext_modules = [libhfst_module],
      py_modules = ["libhfst"],
      packages = ["hfst", "hfst.exceptions", "hfst.sfst_rules", "hfst.xerox_rules"],
      data_files = []
      )
