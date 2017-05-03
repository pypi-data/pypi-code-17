from zenmai.decorators import with_context
from zenmai.utils import quote


@with_context
def load(d, context, format=None, **bindings):
    """
    $load: "./a.yaml#/a"
    """
    return _load(d, context, bindings=bindings, dynamicscope=False, format=format)


@with_context
def load_with_dynamicscope(d, context, format=None, **bindings):
    return _load(d, context, bindings=bindings, dynamicscope=True, format=format)


def _load(d, context, bindings, dynamicscope=False, format=None):
    def onload(filename, loaded):
        if dynamicscope:
            subcontext = context.new_child(filename)
        else:
            subcontext = context.new_child(filename, scope=context.rootscope)
        for k, v in bindings.items():
            subcontext.assign(k, v)
        return context.evaluator.eval(subcontext, loaded)
    r = context.loader.load(d, onload, format=format)
    return quote(r)
