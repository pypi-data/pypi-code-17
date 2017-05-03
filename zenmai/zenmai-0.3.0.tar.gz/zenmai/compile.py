# -*- coding:utf-8 -*-
from zenmai.core import Context, Evaluator, Loader


def compile(d, module, filename=None, evaluator_factory=Evaluator, loader_factory=Loader, context_factory=Context):
    evalator = evaluator_factory()
    loader = loader_factory(d, rootfile=filename)
    context = context_factory(module, loader, evalator, filename=filename)
    return evalator.eval(context, d)
