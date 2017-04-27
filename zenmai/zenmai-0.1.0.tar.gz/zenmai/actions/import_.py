from zenmai.langhelpers import import_module
from zenmai.decorators import (
    with_context,
    sideeffect,
)


@with_context
@sideeffect
def import_(s, context, as_=None):
    """
    $import: "zenmai.actions.suffix"
    as: s

    $s.suffix:
      name: foo
    """
    imported = import_module(s, here=context.filename)
    as_ = as_ or s.split(".")[0]
    context.assign(as_, imported)
