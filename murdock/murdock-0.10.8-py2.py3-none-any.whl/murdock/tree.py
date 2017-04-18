# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Module `murdock.tree`
---------------------

A module to organize atoms into directed graphs (`trees`_) using connected
`.Node` instances.

.. _trees: http://en.wikipedia.org/wiki/Tree_(graph_theory)

The directed graph - build as a network of `.Node` instances - can be used
whenever parts of a `~.molstruct.MolecularStructure` (or more general a list of
`~.molstruct.Atom` instances) are modified so that properties (i.e.
coordinates) between atoms within the modified part do not change relatively to
each other but do change relatively to all other atoms of the
`~.molstruct.MolecularStructure` (or `~.molstruct.Atom` list). If e.g. a
sidechain of a ligand is rotated, the graph gives immediate access to all atoms
which have changed relatively to that sidechain (rest of the ligand + receptor)
and the corresponding interaction energies can be calculated.

Each `.Node` can have one `~.Node.parent` and a list of `~.Node.children`,
which are all `.Node` instances themselves, thus building a directed graph with
one root (`.Node` without a `~.Node.parent`), a number of inner nodes and,
finally, a number of `~.Node.leaves()` (`.Node` instance without
`~.Node.children`). Each `.Node` holds a list of `~.Node.atoms` - references to
`~.molstruct.Atom` instances -  where the `~.Node.atoms` of a `~.Node.parent`
are distributed between their `~.Node.children`.

Examples:
    Create a root `.Node` and put in a receptor-ligand system:
        >>> system = Node(name='system')
        >>> receptor = Node(name='receptor', parent=system)
        >>> ligand = Node(name='ligand', parent=system)

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.utils import viewitems

import logging

import numpy

import murdock.math
import murdock.transforms


log = logging.getLogger(__name__)


class TreeError(Exception):
    pass


class Node(object):
    """A class representing a node within a directed graph.
    """

    def __init__(
            self, name='unnamed', parent=None, source=None, static=True,
            object_serial=None):
        #: list of child `.Node` instances
        self.children = []
        #: list of `~.molstruct.Atom` instances contained
        self.atoms = []
        #: name of this `.Node`
        self.name = name
        #: parent `.Node`
        self.parent = parent
        if parent:
            parent.add_node(self)
        #: a unique integer identifier for each physically connected object
        #: within a tree structure
        self.object_serial = object_serial
        #: list of bonds (`~.molstruct.Bond`) in the node
        self.bonds = []
        #: list of `~.transforms.Transformation` instances associated with this
        #: node
        self.transforms = []
        #: reference to a source object (e.g. another Node or a
        #: `~.molstruct.Molstruct()`)
        self.source = source
        #: defines whether the node or any descendant have any
        #: `.transforms`
        self.static = static

    def __str__(self):
        if self.parent:
            pname = self.parent.name
        else:
            pname = None
        return (
            'Type: {ctype}\nName: {name}\nParent name: {pname}\n'
            'Number of children: {num_child}\nNumber of atoms: {num_at}\n'
            'Number of unrelated nodes: {num_unrel_node}'.format(
                ctype=type(self), name=self.name, pname=pname,
                num_child=len(self.children), num_at=len(self.atoms),
                num_unrel_node=sum(1 for _u in self.unrelated())))

    def add_atom(self, atom):
        """Add atom to `.atoms` and update ancestors `.atoms` lists.
        """
        if atom in self.atoms:
            raise TreeError(
                'Atom `%s` can not be added to node `%s`, its already in '
                'there.' % (atom.name, self.name))
        self.atoms.append(atom)
        if self.parent:
            self.parent.add_atom(atom)
        return True

    def add_atoms(self, atoms):
        """Extend `.atoms` by the list given as `atoms`.
        """
        for atom in atoms:
            self.add_atom(atom)
        return True

    def add_bond(self, bond):
        """Add bond to `.bonds` and update ancestors `.bonds` lists.

        Because bonds are shared between atoms the ancestors lists need to be
        checked before adding a bond, which maked this function save but very
        expensive.

        """
        if bond not in self.bonds:
            self.bonds.append(bond)
        if self.parent:
            self.parent.add_bond(bond)
        return True

    def add_transformation(self, tf):
        """Add `~.transforms.Transformation` instance.
        """
        self.transforms.append(tf)
        self.set_as_dynamic()
        return True

    def add_node(self, node):
        self.add_atoms(node.atoms)
        if node in self.children:
            raise TreeError(
                'Node `%s` can not be added to node `%s`, its already one of '
                'the children.' % (node.name, self.name))
        self.children.append(node)
        return True

    def descendant_transforms(self):
        return [
            _tf for _node in self.descendants() for _tf in _node.transforms]

    def descendants(self):
        """Iterate over all descendent nodes (children, grandchildren, ...).
        """
        for child in self.children:
            yield child
            if child.children:
                for grandchild in child.descendants():
                    yield grandchild

    def deepcopy(self, parent=None, suffix='', inner_recursion=False):
        """Return a deepcopy of the full tree.
        """
        new_node = Node(
            name='%s%s' % (self.name, suffix), parent=parent,
            static=self.static, object_serial=self.object_serial)
        new_node.source = self
        if self.children:
            for child in self.children:
                child.deepcopy(
                    parent=new_node, inner_recursion=True, suffix=suffix)
        if inner_recursion:
            return new_node
        mappings = {}
        for d, new_d in zip(self.iternodes(), new_node.iternodes()):
            for atom in d.atoms:
                if atom in mappings:
                    new_atom = mappings[atom]
                else:
                    new_atom = atom.deepcopy()
                    mappings[atom] = new_atom
                new_d.atoms.append(new_atom)
        for d, new_d in zip(self.iternodes(), new_node.iternodes()):
            for bond in d.bonds:
                if bond in mappings:
                    new_bond = mappings[bond]
                else:
                    atoms = [mappings[_a] for _a in bond.atoms]
                    if bond.tors_atoms is None:
                        tors_atoms = None
                    else:
                        tors_atoms = [
                            mappings[_a] for _a in bond.tors_atoms]
                    new_bond = bond.deepcopy(
                        atoms=atoms, tors_atoms=tors_atoms)
                    for atom in atoms:
                        atom.add_bond(new_bond)
                    mappings[bond] = new_bond
                new_d.bonds.append(new_bond)
        for node in new_node.iternodes():
            for tf in node.source.transforms:
                new_tf = tf.deepcopy(
                    node=node, mappings=mappings, suffix=suffix)
                node.add_transformation(new_tf)
        return new_node

    def dynamic_atoms(self):
        """Return all atoms in `self` which belong to a dynamic node.
        """
        if not self.static:
            return self.atoms
        atoms = []
        for leaf in self.leaves():
            if not leaf.static:
                atoms.extend([_atom for _atom in leaf.atoms])
        return atoms

    def fork(self, atom_lists, names=None):
        """Fork the `.Node` instance into multiple children nodes.

        The parameter ``atom_lists`` contains n exclusive lists of atoms within
        the parent instance. To avoid performance loss those lists are NOT
        checked for double occurances of atoms! This has to be avoided by the
        user as ambiguous lists will cause errors.

        To fork the node, multiple `.Node` instances are created and added to
        the parent `.Node` as new children. If there are atoms contained in the
        parent but in none of the children, one additional child is created to
        contain those remaining atoms.

        """
        if self.children:
            raise TreeError(
                'Only leaves (nodes without children) can be forked!')
        if names:
            names = names[:]
        all_atoms = []
        nodes = []
        # Check whether any of the atom lists includes all atoms of `node`
        for i, atom_list in enumerate(atom_lists):
            all_atoms.extend(atom_list)
            if len(atom_list) >= len(self.atoms):
                raise TreeError(
                    'Can not fork node `%s` (%d atoms) using `atom_lists[%d]` '
                    '(%d atoms)!' %
                    (self.name, len(self.atoms), i, len(atom_list)))
        # Check for the correct number of names, one for each element of
        # `atom_lists`. One name for the remaining atoms is added if necessary.
        if names:
            if len(atom_lists) == len(names):
                names.append('unnamed')
            elif len(atom_lists) != len(names) - 1:
                raise TreeError(
                    'The optional name list in `fork` (if given) must have '
                    'the same number of elements as there are atom lists, or '
                    'one more if there are remaining atoms in the node being '
                    'forked, not contained within any of atom lists.')
        else:
            names = [
                '%s_%d' % (self.name, _i) for _i, _a in enumerate(atom_lists)]
            names.append('%s_%d' % (self.name, len(names)))
        # Check for remaining atoms and add an additional list (and node) for
        # them if required.
        remaining_atoms = [_a for _a in self.atoms if _a not in all_atoms]
        if remaining_atoms:
            atom_lists.append(remaining_atoms)
        # Create new nodes (children).
        for i, atom_list in enumerate(atom_lists):
            new_node = Node(
                parent=self, name=names[i], static=self.static,
                object_serial=self.object_serial)
            #: Expensive iterations necessary to conserve atom and bond order
            for atom in self.atoms:
                if atom in atom_list:
                    new_node.atoms.append(atom)
            for bond in self.bonds:
                for atom in atom_list:
                    if bond in atom.bonds:
                        new_node.bonds.append(bond)
                        break
            nodes.append(new_node)
        return nodes

    def init_rotbonds(self, bonds, scaling, max_step=None):
        """Create a full torsional tree from rotatable bonds.

        A list of rotatable bonds is given in the form of tuples
        (atom1, atom2). The node is forked at each rotatable bond given
        in `bonds` and one rotational degree of freedom per bond is added.

        """
        tors_root = self.torsional_root()
        # Initialize list of bonds already made rotatable.
        done = []
        # Iterate through structure, from tors_root outwards.
        for atom in tors_root.connected():
            # Check which bonds of `atom` to make rotatable.
            for bond in atom.bonds:
                if bond not in bonds or bond in done:
                    continue
                done.append(bond)
                # Select subtree on one side of the bond.
                sub = bond.atoms[1].connected(no_go=[bond.atoms[0]])
                # Make sure it is the side opposing the root atom.
                if tors_root in sub:
                    sub = bond.atoms[0].connected(no_go=[bond.atoms[1]])
                parent = None
                # Look for leaf to be forked.
                for leaf in self.leaves():
                    fit = True
                    for atom in sub:
                        if atom not in leaf.atoms:
                            fit = False
                            break
                    if fit is True:
                        parent = leaf
                        break
                if parent is None:
                    raise TreeError('No leaf holding all atoms found!')
                # Fork leaf
                rotatable = parent.fork([sub])[0]
                if bond.unbonded is None:
                    offset = None
                else:
                    offset = -bond.unbonded.angle()
                tf = murdock.transforms.BondRotation(
                    node=rotatable, max_step=max_step, name=bond.name,
                    offset=offset, scaling=scaling, bond=bond)
                rotatable.add_transformation(tf)
        return True

    def iternodes(self):
        """Iterate over `self` and all `.descendent` nodes.
        """
        yield self
        for node in self.descendants():
            yield node

    def leaves(self):
        """Iterate over all leaves.

          .. seealso:: http://en.wikipedia.org/wiki/Tree_(graph_theory)

        """
        if not self.children:
            yield self
        else:
            for child in self.children:
                for leaf in child.leaves():
                    yield leaf

    def residue_data(self, node):
        res_dicts = []
        for obj_serial, node in enumerate((self, node)):
            d = {}
            for atom in node.atoms:
                res = atom.source_atom.residue
                if res not in d:
                    d[res] = Node(object_serial=obj_serial)
                d[res].add_atom(atom)
            res_dicts.append(d)
        return res_dicts

    def residue_distances(self, node):
        res_dicts = self.residue_data(node)
        dists1 = {_res: None for _res in res_dicts[0]}
        dists2 = {_res: None for _res in res_dicts[1]}
        for r1, n1 in viewitems(res_dicts[0]):
            for r2, n2 in viewitems(res_dicts[1]):
                d = numpy.min(murdock.math.distmat(n1.atoms, n2.atoms))
                if dists1[r1] is None or dists1[r1] > d:
                    dists1[r1] = d
                if dists2[r2] is None or dists2[r2] > d:
                    dists2[r2] = d
        return dists1, dists2

    def root(self):
        """Return the root of the tree (the ancestor without parent).
        """
        if not self.parent:
            return self
        return self.parent.root()

    def set_as_dynamic(self):
        """Set the `.static` attribute for this instance and all descendants.
        """
        self.static = False
        if self.children:
            for child in self.children:
                child.set_as_dynamic()
        return True

    def static_atoms(self):
        """Return all atoms in `self` which belong to a static node.
        """
        if self.static:
            return self.atoms
        atoms = []
        for leaf in self.leaves():
            if leaf.static:
                atoms.extend([_atom for _atom in leaf.atoms])
        return atoms

    def torsional_root(self):
        """Return the atom with the smallest largest torsional subtree.
        """
        min_max_size = None
        root = None
        bonds_found = 0
        for atom in self.atoms:
            max_size = None
            for batom in atom.bonded:
                bonds_found += 1
                size = len(batom.connected(no_go=[atom]))
                if max_size is None or max_size < size:
                    max_size = size
            if min_max_size is None or max_size < min_max_size:
                min_max_size = max_size
                root = atom
        if bonds_found is 0:
            log.error(
                'No bonds defined for node `%s`. Can not identify the '
                'torsional root atom.', self.name)
            return False
        if root is None:
            log.fatal(
                'Unexpected error in `torsional_root`. Can not identify '
                'torsional root atom for node `%s`.', self.name)
            return False
        return root

    def unrelated(self):
        """Iterate over `nodes` connected to `self` but neither ancestor nor
        descendant.
        """
        own_leaves = [_leaf for _leaf in self.leaves()]
        for leaf in self.root().leaves():
            if leaf not in own_leaves:
                yield leaf

    def update_source(self):
        for atom in self.dynamic_atoms():
            atom.source.coords = atom.coords.copy()
        return True
