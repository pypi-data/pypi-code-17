from collections import namedtuple
import weakref

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

    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
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


def format_tree(node, prefix='', key=None):
    children = node.children

    def make_branch(s, v):
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

    def __init__(self, value):
        self.value = value
        self._parent = None
        self._children = []

    def __repr__(self):
        return 'Node({!r:})'.format(self.value)

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, child):
        self._children.append(child)
        child.parent = self

    def add_children(self, children):
        for child in children:
            self._children.append(child)
            child.parent = self

    def __iter__(self):
        return iter(self._children)

    def build_tree(self):
        return "\n".join([self.value, "\n".join(format_tree(self))])

    def depth_first(self):
        return DepthFirstIterator(self)
