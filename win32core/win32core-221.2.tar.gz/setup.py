'''This is a distutils setup-script for the pywin32 extensions

To build the pywin32 extensions, simply execute:
  python setup.py build
or
  python setup.py install
to build and install into your current Python installation.
'''

from setuptools import setup

try:
    import yaml
    import toposort
except ImportError:
    # we're running on an older pip version, use this hack
    from setuptools.dist import Distribution
    Distribution({'setup_requires': ['pyyaml', 'toposort']})

import os
import re
import string
import versioneer
import shutil
import distutils.util
import distutils.file_util
import versioneer
import textwrap
import glob
import yaml

from copy import copy
from setuptools import find_packages
from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from distutils import log
from distutils.dep_util import newer_group
from distutils.sysconfig import get_config_vars
from contextlib import suppress
from toposort import toposort_flatten
from collections import deque

# prevent the new in 3.5 suffix of 'cpXX-win32' from being added.
# (adjusting both .cp35-win_amd64.pyd and .cp35-win32.pyd to .pyd)
with suppress(KeyError):
    get_config_vars()["EXT_SUFFIX"] = re.sub("\\.cp\d\d-win((32)|(_amd64))",
                                             "",
                                             get_config_vars()["EXT_SUFFIX"])


class WinExt(Extension):
    # Base class for all win32 extensions, with some predefined
    # library and include dirs, and predefined windows libraries.
    # Additionally a method to parse .def files into lists of exported
    # symbols, and to read

    def __init__(
            self,
            name,
            sources,
            include_dirs=[],
            define_macros=None,
            undef_macros=None,
            library_dirs=[],
            libraries=[],
            runtime_library_dirs=None,
            extra_objects=None,
            extra_compile_args=None,
            extra_link_args=None,
            export_symbols=None,
            export_symbol_file=None,
            pch_header=None,
            windows_h_version=None,  # min version of windows.h needed.
            extra_swig_commands=None,
            is_regular_dll=False,  # regular Windows DLL?
            # list of headers which may not be installed forcing us to
            # skip this extension
            optional_headers=[],
            depends=None,
            platforms=None,  # none means 'all platforms'
            unicode_mode=None,
            # 'none'==default or specifically true/false.
            implib_name=None,
            delay_load_libraries=''):

        self.delay_load_libraries = delay_load_libraries.split()
        libraries.extend(self.delay_load_libraries)

        if export_symbol_file:
            export_symbols = export_symbols or []
            export_symbols.extend(self.parse_def_file(export_symbol_file))

        # Some of our swigged files behave differently in distutils vs
        # MSVC based builds.  Always define DISTUTILS_BUILD so they can tell.
        define_macros = define_macros or []
        define_macros.append(('DISTUTILS_BUILD', None))
        define_macros.append(('_CRT_SECURE_NO_WARNINGS', None))

        self.pch_header = pch_header
        self.extra_swig_commands = extra_swig_commands or []
        self.windows_h_version = windows_h_version
        self.optional_headers = optional_headers
        self.is_regular_dll = is_regular_dll
        self.platforms = platforms
        self.implib_name = implib_name
        Extension.__init__(self, name, sources, include_dirs, define_macros,
                           undef_macros, library_dirs, libraries,
                           runtime_library_dirs, extra_objects,
                           extra_compile_args, extra_link_args, export_symbols)

        if not hasattr(self, 'swig_deps'):
            self.swig_deps = []
        self.extra_compile_args.extend(['/DUNICODE', '/D_UNICODE', '/DWINNT'])
        self.unicode_mode = unicode_mode

        if self.delay_load_libraries:
            self.libraries.append('delayimp')
            for delay_lib in self.delay_load_libraries:
                self.extra_link_args.append('/delayload:%s.dll' % delay_lib)

        if not hasattr(self, '_needs_stub'):
            self._needs_stub = False

    def parse_def_file(self, path):
        # Extract symbols to export from a def-file
        result = []
        for line in open(path).readlines():
            line = line.rstrip()
            if line and line[0] in string.whitespace:
                tokens = line.split()
                if not tokens[0][0] in string.ascii_letters:
                    continue
                result.append(','.join(tokens))
        return result


################################################################
# Extensions to the distutils commands.


class my_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        self.windows_h_version = None
        self.excluded_extensions = []  # list of (ext, why)
        self.swig_cpp = True  # hrm - deprecated - should use swig_opts=-c++??
        if not hasattr(self, 'plat_name'):
            # Old Python version that doesn't support cross-compile
            self.plat_name = distutils.util.get_platform()

        for ext in self.extensions:
            self.library_dirs.append(
                os.path.join(self.build_temp, ext.name, 'src'))

    def run(self):
        build_ext.run(self)

    def build_extensions(self):
        # First, sanity-check the 'extensions' list
        self.check_extensions_list(self.extensions)
        self.found_libraries = {}

        if not hasattr(self.compiler, 'initialized'):
            # 2.3 and earlier initialized at construction
            self.compiler.initialized = True
        else:
            if not self.compiler.initialized:
                self.compiler.initialize()

        for ext in self.extensions:
            self.build_extension(ext)

    def find_swig(self):
        if 'SWIG' in os.environ:
            swig = os.environ['SWIG']
        else:
            # We know where our swig is
            swig = os.path.abspath(os.path.join('swig', 'swig.exe'))
        lib = os.path.join(os.path.dirname(swig), 'swig_lib')
        os.environ['SWIG_LIB'] = lib
        return swig

    def swig_sources(self, sources, extension):
        new_sources = []
        swig_sources = []
        swig_targets = {}
        # XXX this drops generated C/C++ files into the source tree, which
        # is fine for developers who want to distribute the generated
        # source -- but there should be an option to put SWIG output in
        # the temp dir.
        # Adding py3k to the mix means we *really* need to move to generating
        # to the temp dir...
        target_ext = '.cpp'
        for source in sources:
            (base, sext) = os.path.splitext(source)
            if sext == '.i':  # SWIG interface file
                if os.path.split(base)[1] in swig_include_files:
                    continue
                swig_sources.append(source)
                # Patch up the filenames for various special cases...
                if os.path.basename(base) in swig_interface_parents:
                    swig_targets[source] = base + target_ext
                else:
                    new_target = '%s_swig%s' % (base, target_ext)
                    new_sources.append(new_target)
                    swig_targets[source] = new_target
            else:
                new_sources.append(source)

        if not swig_sources:
            return new_sources

        swig = self.find_swig()
        for source in swig_sources:
            swig_cmd = [swig, '-python', '-c++']
            swig_cmd.append(
                '-dnone', )  # we never use the .doc files.
            swig_cmd.extend(extension.extra_swig_commands)

            if distutils.util.get_platform() == 'win-amd64':
                swig_cmd.append('-DSWIG_PY64BIT')
            else:
                swig_cmd.append('-DSWIG_PY32BIT')
            target = swig_targets[source]
            with suppress(KeyError):
                interface_parent = swig_interface_parents[os.path.basename(
                    os.path.splitext(source)[0])]

                # Using win32 extensions to SWIG for generating COM classes.
                if interface_parent is not None:
                    # generating a class, not a module.
                    swig_cmd.append('-pythoncom')
                    if interface_parent:
                        # A class deriving from other than the default
                        swig_cmd.extend(
                            ['-com_interface_parent', interface_parent])

            # This 'newer' check helps python 2.2 builds, which otherwise
            # *always* regenerate the .cpp files, meaning every future
            # build for any platform sees these as dirty.
            # This could probably go once we generate .cpp into the temp dir.
            fqsource = os.path.abspath(source)
            fqtarget = os.path.abspath(target)
            rebuild = self.force or (extension and newer_group(
                extension.swig_deps + [fqsource], fqtarget))
            log.debug('should swig %s->%s=%s', source, target, rebuild)
            if rebuild:
                swig_cmd.extend(['-o', fqtarget, fqsource])
                log.info('swigging %s to %s', source, target)
                out_dir = os.path.dirname(source)
                cwd = os.getcwd()
                os.chdir(out_dir)
                try:
                    self.spawn(swig_cmd)
                finally:
                    os.chdir(cwd)
            else:
                log.info('skipping swig of %s', source)

        return new_sources


################################################################

################################################################

# Special definitions for SWIG.
swig_interface_parents = {
    # source file base,     'base class' for generated COM support
    'mapi': None,  # not a class, but module
    'PyIMailUser': 'IMAPIContainer',
    'PyIABContainer': 'IMAPIContainer',
    'PyIAddrBook': 'IMAPIProp',
    'PyIAttach': 'IMAPIProp',
    'PyIDistList': 'IMAPIContainer',
    'PyIMailUser': 'IMAPIContainer',
    'PyIMAPIContainer': 'IMAPIProp',
    'PyIMAPIFolder': 'IMAPIContainer',
    'PyIMAPIProp': '',  # '' == default base
    'PyIMAPISession': '',
    'PyIMAPIStatus': 'IMAPIProp',
    'PyIMAPITable': '',
    'PyIMessage': 'IMAPIProp',
    'PyIMsgServiceAdmin': '',
    'PyIMsgStore': 'IMAPIProp',
    'PyIProfAdmin': '',
    'PyIProfSect': 'IMAPIProp',
    'PyIConverterSession': '',
    # exchange and exchdapi
    'exchange': None,
    'exchdapi': None,
    'PyIExchangeManageStore': '',
    # ADSI
    'adsi': None,  # module
    'PyIADsContainer': 'IDispatch',
    'PyIADsDeleteOps': 'IDispatch',
    'PyIADsUser': 'IADs',
    'PyIDirectoryObject': '',
    'PyIDirectorySearch': '',
    'PyIDsObjectPicker': '',
    'PyIADs': 'IDispatch',
}

# .i files that are #included, and hence are not part of the build.  Our .dsp
# parser isn't smart enough to differentiate these.
swig_include_files = 'mapilib adsilib'.split()


def collect_extensions(parent):
    modules = {}
    dependencies = {}
    build_order = ('.i', '.mc', '.rc', '.cpp')

    for name in os.listdir(parent):
        yml = os.path.join(parent, name, 'module.yml')
        if os.path.isfile(yml):
            with open(yml) as fh:
                cfg = yaml.load(fh)

            modules[name] = cfg
            dependencies[name] = set(cfg.setdefault('modules', []))

    for name in toposort_flatten(dependencies):
        src = os.path.join(parent, name, 'src')
        sources = []
        files = os.listdir(src)

        for item in build_order:
            for fname in files:
                if fname.endswith(item):
                    sources.append(os.path.join(src, fname))

        include_dirs = []
        f = set()
        q = deque([name])

        while q:
            dep = q.popleft()
            include_dirs.extend([
                os.path.join(parent, dep, 'src'), os.path.join(
                    parent, dep, 'include')
            ])
            f.add(dep)
            q.extend([d for d in dependencies[name] if d not in f])

        cfg = modules[name]
        del cfg['modules']

        with suppress(KeyError):
            for i, depend in enumerate(cfg['depends']):
                cfg['depends'][i] = os.path.join(name, 'include', depend)

        for config_option in ['export_symbol_file', 'pch_header']:
            with suppress(KeyError):
                cfg[config_option] = os.path.join(name, 'include',
                                                  cfg[config_option])

        yield WinExt(
            name, sources=sources, include_dirs=copy(include_dirs), **cfg)

        print('Collected {}'.format(name))


################################################################

cmdclass = versioneer.get_cmdclass()
cmdclass.update({
    'build_ext': my_build_ext,
})

setup(
    name='win32core',
    version=versioneer.get_version(),
    description='Python for Window Extensions',
    long_description=textwrap.dedent('''
        Python extensions for Microsoft Windows'
        Provides access to much of the Win32 API, the
        ability to create and use COM objects, and the
        Pythonwin environment
        
        This provides the core functionality.
        '''),
    author='Mark Hammond (et al)',
    author_email='mhammond@users.sourceforge.net',
    url='http://sourceforge.net/projects/pywin32/',
    license='PSF',
    cmdclass=cmdclass,
    ext_modules=list(collect_extensions('.')),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'makepy = win32com.client.makepy:main',
            'verstamp = win32.verstamp:main',
        ],
    })
