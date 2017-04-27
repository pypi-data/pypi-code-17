from dictknife import loading
from zenmai.actions import concat
import zenmai


class Driver:
    def __init__(self, module, srcfile, format=None, data=None):
        self.module = module
        self.srcfile = srcfile
        self.format = format
        self.data = data or []

    def transform(self, d):
        def context_factory(*args, **kwargs):
            context = zenmai.Context(*args, **kwargs)
            context.assign("data", concat(self.data))  # xxx
            return context
        return zenmai.compile(d, self.module, filename=self.srcfile, context_factory=context_factory)

    def load(self, fp):
        return loading.load(fp)

    def dump(self, d, fp):
        return loading.dump(d, fp, format=self.format)

    def run(self, inp, outp):
        data = self.load(inp)
        result = self.transform(data)
        self.dump(result, outp)
