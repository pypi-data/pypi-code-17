from ..decorators import with_context
from ..utils import quote


@with_context
def load(d, context, **bindings):
    """
    $load: "./a.yaml#/a"
    """
    def onload(filename, loaded):
        subcontext = context.new_child(filename)
        for k, v in bindings.items():
            subcontext.assign(k, v)
        return context.evaluator.eval(subcontext, loaded)
    r = context.loader.load(d, onload)
    return quote(r)
