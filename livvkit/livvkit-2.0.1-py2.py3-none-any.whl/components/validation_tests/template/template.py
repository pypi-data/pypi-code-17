# Copyright (c) 2015,2016, UT-BATTELLE, LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
This is a template validation test that can be used by developers to create new
validation tests.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from livvkit.util.functions import Optional
from livvkit.util import elements


def run(name, config):
    """
    Runs the analysis.

    Args:
        name: The name of the test
        config: A dictionary representation of the configuration file

    Returns:
       The result of elements.page with the list of elements to display
    """
    # TODO: Put your analysis here
    element_list = elements.error("Unimplemented test", "This test contains no analysis code!")
    return elements.page(name, config['description'], element_list)


@Optional
def print_summary():
    """
    Print out a summary generated by this module's summarize_result method
    """
    raise NotImplementedError


@Optional
def summarize_result():
    """
    Provides a snapshot of the results of the analysis to be provided
    to the sumamry as well as being printed out in this module's
    print_summary method
    """
    raise NotImplementedError


@Optional
def populate_metadata():
    """
    Generates the metadata responsible for telling the summary what
    is done by this module's run method
    """
    raise NotImplementedError
