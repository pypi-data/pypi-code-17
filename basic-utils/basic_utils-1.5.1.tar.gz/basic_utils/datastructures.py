import weakref
from collections import namedtuple
from typing import Any, Callable, Iterable, List, Optional

Branch = namedtuple('Branch', 'obj, value')

FORK = '\u251c'
LAST = '\u2514'
VERTICAL = '\u2502'
SIDE = '\u2500'
NEWLINE = '\u23ce'


class DepthFirstIterator(object):
    """
    Credit:
        Derived from Python Cookbook 3rd Edition by David Beazley
    """

    def __init__(self, start_node: Any) -> None:
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)  # type: ignore
            return self._node
        # If processing a child, return its next item,
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # Advance to the next child and start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


def format_tree(node: 'Node', prefix: str='', key: Callable=None) -> Iterable:
    children = node.children

    def make_branch(s: str, v: str) -> str:
        return ''.join([prefix, s, SIDE * 2, ' ', v])

    if children:
        *branches, last = tuple(children)
        for branch in branches:
            yield make_branch(FORK, branch.value)
            yield from format_tree(branch, prefix + VERTICAL + '   ')
        if last:
            yield make_branch(LAST, last.value)
            yield from format_tree(last, prefix + '    ')


class Node:
    """
    Simple node class, support single inheritence and multiple children

    Credit:
        Derived from Python Cookbook 3rd Edition by David Beazley
    """

    def __init__(self, value: Any) -> None:
        self.value = value
        self._parent = None
        self._children = []  # type: List[Node]

    def __repr__(self) -> str:
        return 'Node({!r:})'.format(self.value)

    @property
    def children(self) -> List['Node']:
        return self._children

    @property
    def parent(self) -> Optional['Node']:
        if self._parent is None:
            return self._parent
        else:
            return self._parent()

    @parent.setter
    def parent(self, node: 'Node') -> None:
        self._parent = weakref.ref(node)  # type: ignore

    def add_child(self, child: 'Node') -> None:
        self._children.append(child)
        child.parent = self

    def add_children(self, children: Iterable['Node']) -> None:
        for child in children:
            self._children.append(child)
            child.parent = self

    def __iter__(self) -> Iterable['Node']:
        return iter(self._children)

    def build_tree(self) -> str:
        return "\n".join([self.value, "\n".join(format_tree(self))])

    def depth_first(self) -> 'DepthFirstIterator':
        return DepthFirstIterator(self)
