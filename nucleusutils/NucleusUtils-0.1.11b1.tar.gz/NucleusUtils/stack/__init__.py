from .link import MemoryLink as _MemoryLink
from .memory import Memory as _Memory
from .stack import Stack as _Stack

memory = _Memory()
main_stack = _Stack()


def link(obj):
    return main_stack.add(obj)


def unlink(link):
    assert isinstance(link, _MemoryLink)
    return link.get()
