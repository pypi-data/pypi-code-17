# -*- coding: utf-8 -*-
import sys
import os
from distutils.core import setup
from setuptools import find_packages

#########
# settings
#########

project_var_name = "jupytalk"
sversion = "0.2"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
requirements = None

KEYWORDS = project_var_name + ', first name, last name'
DESCRIPTION = """Material for presentations. The documentation generation is using pyquickhelper."""


CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]


#######
# data
#######


packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name + ".mokadi.grammars": ["*.g4", "*.tokens"],
                project_var_name + ".mokadi.data": ["*.wav", "*.ico"]}


############
# functions
############


def is_local():
    file = os.path.abspath(__file__).replace("\\", "/").lower()
    if "/temp/" in file and "pip-" in file:
        return False
    if \
       "bdist_msi" in sys.argv or \
       "build27" in sys.argv or \
       "build_script" in sys.argv or \
       "build_sphinx" in sys.argv or \
       "bdist_wheel" in sys.argv or \
       "bdist_wininst" in sys.argv or \
       "clean_pyd" in sys.argv or \
       "clean_space" in sys.argv or \
       "copy27" in sys.argv or \
       "copy_dist" in sys.argv or \
       "local_pypi" in sys.argv or \
       "notebook" in sys.argv or \
       "publish" in sys.argv or \
       "publish_doc" in sys.argv or \
       "register" in sys.argv or \
       "unittests" in sys.argv or \
       "unittests_LONG" in sys.argv or \
       "unittests_SKIP" in sys.argv or \
       "unittests_GUI" in sys.argv or \
       "run27" in sys.argv or \
       "sdist" in sys.argv or \
       "setupdep" in sys.argv or \
       "test_local_pypi" in sys.argv or \
       "upload_docs" in sys.argv or \
       "setup_hook" in sys.argv or \
       "copy_sphinx" in sys.argv or \
       "update_grammars" in sys.argv or \
       "write_version" in sys.argv:
        try:
            import_pyquickhelper()
        except ImportError:
            return False
        return True
    else:
        return False


def import_pyquickhelper():
    try:
        import pyquickhelper
    except ImportError:
        sys.path.append(
            os.path.normpath(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "pyquickhelper" if sys.version_info[
                            0] >= 3 else "py27_pyquickhelper_27",
                        "src"))))
        try:
            import pyquickhelper
        except ImportError as e:
            message = "module pyquickhelper is needed to build the documentation ({0}), not found in path {1}".format(
                sys.executable,
                sys.path[
                    -1])
            raise ImportError(message) from e
    return pyquickhelper


def verbose():
    print("---------------------------------")
    print("package_dir =", package_dir)
    print("packages    =", packages)
    print("package_data=", package_data)
    print("current     =", os.path.abspath(os.getcwd()))
    print("---------------------------------")

##########
# version
##########


if is_local() and "--help" not in sys.argv and "--help-commands" not in sys.argv:
    def write_version():
        pyquickhelper = import_pyquickhelper()
        from pyquickhelper.pycode import write_version_for_setup
        return write_version_for_setup(__file__)

    if sys.version_info[0] != 2:
        write_version()

    version = os.path.join(os.path.dirname(__file__), "version.txt")
    if os.path.exists(version):
        with open(version, "r") as f:
            lines = f.readlines()
        subversion = "." + lines[0].strip("\r\n ")
        if subversion == ".0":
            raise Exception("subversion is wrong: " + subversion)
    else:
        raise FileNotFoundError(version)
else:
    # when the module is installed, no commit number is displayed
    subversion = ""

if "upload" in sys.argv and not subversion:
    # avoid uploading with a wrong subversion number
    try:
        import pyquickhelper
        pyq = True
    except ImportError:
        pyq = False
    raise Exception(
        "subversion is empty, cannot upload, is_local()={0}, pyquickhelper={1}".format(is_local(), pyq))

##############
# common part
##############

if os.path.exists(readme):
    if sys.version_info[0] == 2:
        from codecs import open
    with open(readme, "r", encoding='utf-8-sig') as f:
        long_description = f.read()
else:
    long_description = ""

if "--verbose" in sys.argv:
    verbose()

if is_local():
    pyquickhelper = import_pyquickhelper()
    logging_function = pyquickhelper.get_fLOG()
    from pyquickhelper.pycode import process_standard_options_for_setup
    logging_function(OutputPrint=True)
    if "unittests" in sys.argv and sys.platform.startswith("win"):
        # There is some issues on Windows.
        from PIL import Image as PIL_Image
        assert PIL_Image is not None
    r = process_standard_options_for_setup(
        sys.argv, __file__, project_var_name, layout=["html"],
        unittest_modules=["pyquickhelper", "jyquickhelper"],
        additional_notebook_path=["mlstatpy", "teachpyx",
                                  "pyquickhelper", "jyquickhelper", "pymmails", "ensae_teaching_cs", "pyensae"],
        additional_local_path=["pyquickhelper", "pyensae", "mlstatpy", "teachpyx",
                               "jyquickhelper", "pymmails", "ensae_teaching_cs"],
        requirements=["pyquickhelper", "jyquickhelper", "mlstatpy", "teachpyx",
                      "pymmails", "ensae_teaching_cs", "pyensae"],
        add_htmlhelp=sys.platform.startswith("win"),
        coverage_options=dict(omit=["*exclude*.py"]),
        fLOG=logging_function, covtoken=(
            "989a8320-d21b-47f4-910b-f1fd9b2e5415", "'_UT_35_std' in outfile"),
        nbformats=('ipynb', 'html', 'python', 'rst', 'slides', 'present', 'github'))
    if not r and "update_grammars" in sys.argv:
        # expecting python setup.py update_grammars file
        ind = sys.argv.index("update_grammars")
        if len(sys.argv) <= ind:
            raise Exception(
                "expecting a grammar file: python setup.py update_grammars MokadiGrammar.g4")
        grammar = sys.argv[ind + 1]
        if not os.path.exists(grammar):
            cdir = os.path.abspath(os.path.dirname(__file__))
            g2 = os.path.join(cdir, "src", "jupytalk",
                              "mokadi", "grammars", grammar)
            if not os.path.exists(g2):
                raise FileNotFoundError("{0}\n{1}".format(grammar, g2))
            grammar = g2
        try:
            from pyensae.languages import build_grammar
        except ImportError:
            sys.path.append(os.path.join(
                os.path.dirname(__file__), "..", "pyensae", "src"))
            from pyensae.languages import build_grammar
        build_grammar(grammar, fLOG=logging_function)
        r = True
    if not r and not ({"bdist_msi", "sdist",
                       "bdist_wheel", "publish", "publish_doc", "register",
                       "upload_docs", "bdist_wininst"} & set(sys.argv)):
        raise Exception("unable to interpret command line: " + str(sys.argv))
else:
    r = False

if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        pyquickhelper = import_pyquickhelper()
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)

    setup(
        name=project_var_name,
        version='%s%s' % (sversion, subversion),
        author='Xavier Dupré',
        author_email='xavier.dupre@gmail.com',
        url="http://www.xavierdupre.fr/app/jupytalk/helpsphinx/index.html",
        download_url="https://github.com/sdpython/jupytalk",
        description=DESCRIPTION,
        long_description=long_description,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=packages,
        package_dir=package_dir,
        package_data=package_data,
        #data_files              = data_files,
        install_requires=['pyquickhelper', "jyquickhelper"],
        #include_package_data    = True,
    )
