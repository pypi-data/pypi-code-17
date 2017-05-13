# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import hashlib


class HashedStorageMixin(object):
    def _save(self, name, content, *args, **kw):
        hashv = hashlib.sha1(content.read()).hexdigest()
        hashv = hashv[:2] + os.path.sep + hashv[2:]
        ext = os.path.splitext(name)[1]
        dirname = os.path.dirname(name)
        filename = os.path.join(dirname, hashv + ext)
        return super(HashedStorageMixin, self)._save(filename, content)

    def generate_filename(self, filename):
        if os.path.isabs(filename):
            raise ValueError('absolute path is Forbidden! "%s"' % filename)
        return super(HashedStorageMixin, self).generate_filename(filename)
