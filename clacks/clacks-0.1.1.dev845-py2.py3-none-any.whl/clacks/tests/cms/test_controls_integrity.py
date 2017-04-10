#!/usr/bin/env python3

"""Control subclasses API compatibility tests"""

from nose.tools import eq_


class TestControlsIntegrity(object):

    """Control subclasses API compatibility tests"""

    def setUp(self):
        """Begin temporary transaction"""
        from gtcms.core.db import db
        db.begin_nested()


    def teardown(self):
        """Rollback temporary transaction"""
        from gtcms.core.db import db
        db.rollback()


    def test_controlName_method_existence(self):
        """Check if all Control subclasses have controlName() method reimplemented"""

        from gtcms.models import Control
        for control in [c for c in Control.__subclasses__()]:
            if issubclass(control, Control):
                try:
                    eq_(control.controlName() != '', True, msg='For class %s' % (control.__name__,))
                except TypeError:
                    raise Exception("TypeError for:", control)


    def test_properties(self):
        """Hmmm. Needs to be moved somewhere (or it is duplicate."""
        from gtcms.core.db import db
        from gtcms.models import BoxControl
        bc = BoxControl()
        db.add(bc)
        bc.properties['abc'] = 'def'
        bc.properties['abd'] = 'fgh'
        db.flush()
        db.expire_all()
        eq_(bc.properties, {'abc': 'def', 'abd': 'fgh'})
        eq_((bc._properties['abc'].name, bc._properties['abc'].value), ('abc', 'def'))
