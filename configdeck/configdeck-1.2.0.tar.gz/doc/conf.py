# -*- coding: utf-8 -*-
#
# configdeck documentation build configuration file
#

import sys
import os.path

# import configdeck, to introspect the version string
sys.path.insert(0, os.path.abspath('..'))
import configdeck

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '_ext')))

#
# General configuration.
#

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'configdeck'
copyright = u'© 2009–2017 Ben Finney and others.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
with open(os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"VERSION")) as version_datafile:
    release = version_datafile.read().strip()
version = release

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['configdeck.']

#
# Options for HTML output.
#

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'configdeckdoc'

#
# Options for LaTeX output.
#

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, doc_class [howto/manual]).
latex_documents = [
  ('index', 'configdeck.tex', u'configdeck Documentation',
   u'Ricardo Kirkner, John R. Lenton', 'manual'),
]
