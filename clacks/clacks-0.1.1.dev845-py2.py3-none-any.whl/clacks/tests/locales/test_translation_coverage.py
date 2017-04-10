#!/usr/bin/env python3

"""Test if there are any mappers left in config."""

from gtcms.core import ROOTPATH
from nose.tools import eq_


class TestGrants(object):

    """Test if there are any mappers left in config."""

    def test_translation_coverage(self):
        """Test if there are any mappers left in config."""
        import polib
        #eq_(dbgrants, set(Grant.systemGrants().keys()))

        for pth in (ROOTPATH/'.gt/custom/locale').glob('??/*.po'):
            if not (pth.parent / '.gt-optional').is_file():
                pofile = polib.pofile(str(pth), wrapwidth=78)
                eq_([], [pth.parts[-2:]+(p.msgid,) for p in pofile
                         if 'fuzzy' in p.flags or not p.translated()])
