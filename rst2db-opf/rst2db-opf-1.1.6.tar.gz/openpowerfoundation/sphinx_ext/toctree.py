# -*- coding: utf-8 -*-
# Copyright (c) 2017 OpenPOWER Foundation
# All rights reserved.
#
# Written by Jeff Scheel <scheel@us.ibm.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
    sphinxcontrib.toctree
    =====================

    This extension provides a directive to handle toctree directives when building docs

    .. moduleauthor::  Jeff Scheel  <scheel@us.ibm.com>
"""

import sys
import os
import glob

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives import flag, unchanged, positive_int
from sphinx.util import docname_join

__version__ = '0.1'

def _print_error(text, node = None):
    """Prints an error string and optionally, the node being worked on."""
    sys.stderr.write('\n%s: %s\n' % (__name__, text))
    if node:
        sys.stderr.write(u"  %s\n" % unicode(node))

class toctree(nodes.Element):
    pass


class TOCTreeDirective(rst.Directive):
    has_content = True
    final_argument_whitespace = True
    required_arguments = 0
    optional_arguments = 0

    option_spec = dict(numbered=flag, titlesonly=flag, glob=flag,
                       reversed=flag, hidden=flag, includehidden=flag,
                       maxdepth=positive_int, name=unchanged, caption=unchanged)    

    def run(self):
        # _print_error("TOCTReeDirective.run: arguments -- ", self.arguments)
        # _print_error("TOCTReeDirective.run: options -- ", self.options)
        # _print_error("TOCTReeDirective.run: contents -- ", self.content)
        # _print_error("TOCTReeDirective.run: self -- ", self)
        
        node = toctree()
        
        # Retrieve options.  Note: not all all implemented!  Only need "glob" at
        # this time.
        node['numbered'] = 'numbered' in self.options
        node['titlesonly'] = 'titlesonly' in self.options
        node['glob'] = 'glob' in self.options
        node['reversed'] = 'reversed' in self.options
        node['hidden'] = 'hidden' in self.options
        node['includehidden'] = 'includehidden' in self.options
        node['maxdepth'] = self.options.get('maxdepth', 99)
        node['name'] = self.options.get('name', '')
        node['caption'] = self.options.get('caption', '')

        # Capture environment
        env = self.state.document.settings.env
        _, cwd = env.relfn2path('/')
        node['working_directory'] = os.path.join(cwd, '')
        source = self.state.document.settings._source
        node['source'] = os.path.splitext(os.path.basename(source))[0]
        source_path = os.path.join(os.path.dirname(source),'')
        node['source_path'] = source_path
        if node['working_directory'] == node['source_path']:
            node['docname'] = node['source']
        else:
            node['docname'] = os.path.join(os.path.relpath(source_path, cwd),node['source'])
        
        # Expand TOC Tree, preserving order where it exists
        toc_files = []
        includefiles = []
        for file in self.content:
            exp_files = []
            source_files = []
            if '*' in file or '?' in file or '[' in file or ']' in file:
                tmp_file_list = glob.glob(source_path+file+'.rst')
                
                # Shorten expanded list of files back to relative path and base names
                for include_file in tmp_file_list:
                    # Extract starting path
                    tmp_file = include_file.replace(source_path,"")
                    
                    # Remove trailing file name
                    if tmp_file.endswith('.rst'):
                        tmp_file = tmp_file[:-4]
                        
                    # Don't include current file in list, add to both lists
                    if node['source'] != tmp_file:
                        exp_files.append(tmp_file)
                        source_files.append(docname_join(env.docname, tmp_file))
                        
                # Sort list alphabetically
                exp_files = sorted(exp_files, key=unicode.lower)
                source_files = sorted(source_files, key=unicode.lower)
                
            else:
                exp_files.append(file)
                source_files.append(docname_join(env.docname, file))
            toc_files = toc_files + exp_files
            includefiles = includefiles + source_files
        
        if toc_files != []:
            node['files'] = toc_files

        # Manually add included files to rebuild list
        for includefile in includefiles:
            # note that if the included file is rebuilt, this one must be
            # too (since the TOC of the included file could have changed)
            env.files_to_rebuild.setdefault(includefile, set()).add(node['docname'])

        return [node]

