from setuptools import setup, find_packages, Extension

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


# extension modules
import numpy
npinc = numpy.get_include()
upfirdn_resampler = Extension("libsquiggly.resampling.upfirdn._Resampler",
    ["libsquiggly/resampling/upfirdn/Resampler_wrap.cpp"],
    include_dirs=[npinc],
)

talkbox_cffilter = Extension("libsquiggly.instfreq.talkbox.tools.cffilter",
    ["libsquiggly/instfreq/talkbox/tools/src/cffilter.c"],
    include_dirs=[npinc],
)

talkbox_cacorr = Extension("libsquiggly.instfreq.talkbox.tools.cacorr",
    ["libsquiggly/instfreq/talkbox/tools/src/cacorr.c"],
    include_dirs=[npinc],
)

#talkbox_clpc = ('clpc', {'sources': ['libsquiggly/instfreq/talkbox/linpred/src/levinson.c']})

talkbox_lpc = Extension('libsquiggly.instfreq.talkbox.linpred._lpc',
    ["libsquiggly/instfreq/talkbox/linpred/src/_lpc.c", 'libsquiggly/instfreq/talkbox/linpred/src/levinson.c'],
    include_dirs=[npinc],
)

setup(
    name = 'libsquiggly',
    version = '1.0.4',
    description = 'A toolbox to answer the age-old question "Why do the squiggly lines do what they do?"',
    long_description = readme,
    author = 'Elliot Saba',
    author_email = 'staticfloat@gmail.com',
    url = 'https://gitlab.cs.washington.edu/ubicomplab/libsquiggly',
    license = license,
    packages = find_packages(exclude=('tests', 'docs')),
    test_suite = "libsquiggly.tests",
    #libraries = [talkbox_clpc],
    ext_modules = [upfirdn_resampler, talkbox_cffilter, talkbox_cacorr, talkbox_lpc],
    install_requires = requirements,
)
