from zenmai.decorators import with_context
from zenmai.utils import quote


@with_context
def load(d, context, format=None, **bindings):
    """
    $load: "./a.yaml#/a"
    """
    def onload(filename, loaded):
        subcontext = context.new_child(filename)
        for k, v in bindings.items():
            subcontext.assign(k, v)
        return context.evaluator.eval(subcontext, loaded)
    r = context.loader.load(d, onload, format=format)
    return quote(r)
