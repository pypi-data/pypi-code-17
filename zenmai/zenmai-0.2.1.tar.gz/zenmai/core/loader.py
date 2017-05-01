import logging
from dictknife.jsonknife import get_resolver_from_filename
from dictknife.jsonknife.accessor import StackedAccessor


logger = logging.getLogger(__name__)


class Loader(object):
    def __init__(self, doc, rootfile):
        self.resolver = get_resolver_from_filename(rootfile, doc=doc)
        self.accessor = StackedAccessor(self.resolver)

    @property
    def data(self):
        return self.resolver.doc

    def load(self, ref, callback, format=None):
        try:
            loaded = self.accessor.access(ref, format=format)
            filename = self.accessor.resolver.filename
            logger.debug("@push load stack %s%s", " " * len(self.accessor.stack), self.accessor.resolver.rawfilename)
            return callback(filename, loaded)
        finally:
            resolver = self.accessor.pop_stack()
            logger.debug("@pop  load stack %s%s", " " * len(self.accessor.stack), resolver.rawfilename)
