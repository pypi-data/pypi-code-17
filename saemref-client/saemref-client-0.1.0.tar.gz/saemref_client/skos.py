"""SKOS concepts harvesting from SAEM-Ref OAI-PMH repository"""

from __future__ import print_function

import os
from os import path

from . import _oai_save_records


def fetch_concepts(url, scheme, output, **kwargs):
    """Retrieve SKOS schemes through OAI-PMH."""

    outdir = path.join(output, scheme.replace('/', '-'))
    if not path.isdir(outdir):
        os.makedirs(outdir)

    _oai_save_records(outdir, url, 'rdef', 'concept:in_scheme:{0}'.format(scheme),
                      **kwargs)
