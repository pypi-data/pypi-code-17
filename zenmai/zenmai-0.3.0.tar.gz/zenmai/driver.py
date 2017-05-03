from dictknife import loading
from dictknife import deepmerge
from zenmai.compile import compile
from zenmai.core import Context, Evaluator, Loader


class Driver:
    evaluator_factory = Evaluator
    loader_factory = Loader

    def __init__(self, module, srcfile, format=None, data=None):
        self.module = module
        self.srcfile = srcfile
        self.format = format
        self.data = data or []

    def context_factory(self, *args, **kwargs):
        context = Context(*args, **kwargs)
        context.assign("data", deepmerge(*self.data, override=False))  # xxx
        return context

    def transform(self, d, wrap=None):
        r = compile(
            d, self.module, filename=self.srcfile,
            evaluator_factory=self.evaluator_factory,
            loader_factory=self.loader_factory,
            context_factory=self.context_factory,
        )
        if wrap is not None:
            r = wrap(r)
        return r

    def load(self, fp):
        return loading.load(fp)

    def dump(self, d, fp):
        return loading.dump(d, fp, format=self.format)

    def run(self, inp, outp, wrap=None):
        data = self.load(inp)
        result = self.transform(data, wrap=wrap)
        self.dump(result, outp)
