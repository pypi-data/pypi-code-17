from zenmai.langhelpers import import_module
from zenmai.decorators import (
    with_context,
    sideeffect,
)


@with_context
@sideeffect
def from_(s, import_, context):
    """
    $from: "zenmai.actions.suffix"
    import: suffix

    $suffix:
      name: foo
    """
    imported = import_module(s, here=context.filename)
    names = import_
    if not isinstance(names, (list, tuple)):
        names = [names]
    for name in names:
        member = getattr(imported, name)
        context.assign(name, member)
