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

"""A set of `pytest` routines for the `.scoring` module.

All classes defined in :mod:`murdock.scoring.pool` are tested individually and
in combination.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.utils import viewitems

import importlib
import os

import pytest
from scipy.constants import pi

import murdock.moldata
import murdock.tree


NDIGITS = 10

INPUT_PATH = os.path.join(os.path.dirname(__file__), 'input')

STRUCT_FILEPATHS = [
    (os.path.join(INPUT_PATH, 'ligand1.mol2'), os.path.join(INPUT_PATH, 'receptor1.mol2'))
]

AMOUNTS = (-10., -1., -0.1, 0., 0.1, 1., 10.)

SCORING_SETUP_NAMES = ["scoring_custom"]

SCORING_SETUPS = {
    "scoring_custom": (
        "murdock.scoring.custom",
        {
            "terms": [
                {
                    "class": "IntraCollision",
                    "parameters": {
                        "weight": 1.0,
                        "van_der_waals_radius_correction_factor": 1.0
                    }
                },
                {
                    "class": "InterCollision",
                    "parameters": {
                        "weight": 1.0,
                        "van_der_waals_radius_correction_factor": 1.0
                    }
                },
                {
                    "class": "Coulomb",
                    "parameters": {
                        "weight": 1.0,
                        "inter": True,
                        "intra": True
                    }
                },
                {
                    "class": "Shape2",
                    "parameters": {"weight": 1.0}
                },
                {
                    "class": "Shape4",
                    "parameters": {"weight": 1.0}
                },
                {
                    "class": "Shape6",
                    "parameters": {"weight": 1.0}
                },
                {
                    "class": "Shape8",
                    "parameters": {"weight": 1.0}
                },
                {
                    "class": "ScreenedCoulomb",
                    "parameters": {
                        "weight": 1.0,
                        "inter": True,
                        "intra": True
                    }
                },
                {
                    "class": "Torque",
                    "parameters": {"weight": 1.0}
                },
                {
                    "class": "Torsional",
                    "parameters": {"weight": 1.0}
                }
            ]
        }
    )
}


@pytest.fixture(scope='module', params=SCORING_SETUP_NAMES)
def scoring_setup(request):
    module = importlib.import_module(SCORING_SETUPS[request.param][0])
    return module, request.param


@pytest.fixture(scope='module', params=STRUCT_FILEPATHS)
def molstructs(request):
    lig = murdock.moldata.get_molstruct(filepath=request.param[0])
    rec = murdock.moldata.get_molstruct(filepath=request.param[1])
    return lig, rec


def molstruct_to_node(molstruct):
    node = murdock.tree.Node(
        name=molstruct.name, parent=None, object_serial=None)
    node.add_atoms(molstruct.atoms())
    for bond in molstruct.bonds():
        node.add_bond(bond)
    return node


def add_default_transforms_to_node(node):
    add_translation_to_node(node)
    add_rotation_to_node(node)
    add_bondrotation_to_node(node)


def add_translation_to_node(node):
    node.set_as_dynamic()
    trans_tf = murdock.transforms.Translation(node=node, scaling=10.0)
    node.add_transformation(trans_tf)


def add_rotation_to_node(node):
    node.set_as_dynamic()
    self_rot_tf = murdock.transforms.Rotation(node=node, scaling=pi)
    node.add_transformation(self_rot_tf)


def add_bondrotation_to_node(node):
    select = [{'rotatable': True}]
    bonds = murdock.molstruct.get_bonds(
        node.bonds, receptor=False, select=select)
    node.init_rotbonds(bonds=bonds, scaling=pi)


TF_SETUPS = [add_default_transforms_to_node]


class TestScoring(object):
    """Tests for the :class:`~murdock.scoring.Scoring`.
    """

    @pytest.mark.parametrize("tf_setup", TF_SETUPS)
    @pytest.mark.parametrize("amount", AMOUNTS)
    @pytest.mark.parametrize("random_speed", [True, False])
    def test_single_random_transformations(
            self, molstructs, tf_setup, amount, random_speed, scoring_setup):
        ligand_molstruct = molstructs[0]
        receptor_molstruct = molstructs[1]
        sysnode = murdock.tree.Node(name='system', parent=None)
        recnode = molstruct_to_node(receptor_molstruct)
        lignode = molstruct_to_node(ligand_molstruct)
        sysnode.add_node(recnode)
        sysnode.add_node(lignode)
        tf_setup(lignode)
        transforms = [
            _tf for _n in lignode.iternodes() for _tf in _n.transforms]
        scoring_parms = SCORING_SETUPS[scoring_setup[1]][1]
        scoring = scoring_setup[0].Scoring(root=sysnode)
        assert scoring.setup(scoring_parms, docking=None)
        term_vals1 = {
            _key: _value for _t in scoring.terms for _key, _value in
            viewitems(_t.values)}
        term_unwgt1 = [_t.unweighted() for _t in scoring.terms]
        term_wgt1 = [_t.weighted() for _t in scoring.terms]
        total1 = scoring.total()
        for tf in transforms:
            tf.randomize_velocity(amount, random_speed=random_speed)
            tf.step()
            score_change1 = scoring.rescore()
            tf.invert_velocity()
            tf.step()
            score_change2 = scoring.rescore()
            # assert: rescoring yields the negative change from the first step
            assert round(score_change2 + score_change1, NDIGITS) == 0
            term_vals2 = {
                _key: _value for _t in scoring.terms for _key, _value in
                viewitems(_t.values)}
            # assert: all partial, unweighted values have been restored
            assert all([
                round(term_vals1[_key] - term_vals2[_key], NDIGITS) == 0 for
                _key in term_vals1])
            term_unwgt2 = [_t.unweighted() for _t in scoring.terms]
            # assert: all unweighted values have been restored
            assert all([
                round(_v1 - _v2, NDIGITS) == 0 for _v1, _v2 in
                zip(term_unwgt1, term_unwgt2)])
            term_wgt2 = [_t.weighted() for _t in scoring.terms]
            # assert: all weighted values have been restored
            assert all([
                round(_v1 - _v2, NDIGITS) == 0 for _v1, _v2 in
                zip(term_wgt1, term_wgt2)])
            total2 = scoring.total()
            # assert: the total score has been restored
            assert round(total1 - total2, NDIGITS) == 0

    @pytest.mark.parametrize("tf_setup", TF_SETUPS)
    @pytest.mark.parametrize("amount", AMOUNTS)
    @pytest.mark.parametrize("random_speed", [True, False])
    def test_collective_random_transformations(
            self, molstructs, tf_setup, amount, random_speed, scoring_setup):
        ligand_molstruct = molstructs[0]
        receptor_molstruct = molstructs[1]
        sysnode = murdock.tree.Node(name='system', parent=None)
        recnode = molstruct_to_node(receptor_molstruct)
        lignode = molstruct_to_node(ligand_molstruct)
        sysnode.add_node(recnode)
        sysnode.add_node(lignode)
        tf_setup(lignode)
        transforms = [
            _tf for _n in lignode.iternodes() for _tf in _n.transforms]
        scoring_parms = SCORING_SETUPS[scoring_setup[1]][1]
        scoring = scoring_setup[0].Scoring(root=sysnode)
        assert scoring.setup(scoring_parms, docking=None)
        term_vals1 = {
            _key: _value for _t in scoring.terms for _key, _value in
            viewitems(_t.values)}
        term_unwgt1 = [_t.unweighted() for _t in scoring.terms]
        term_wgt1 = [_t.weighted() for _t in scoring.terms]
        total1 = scoring.total()
        score_change1 = 0
        for tf in transforms:
            tf.randomize_velocity(amount, random_speed=random_speed)
            tf.step()
            score_change1 += scoring.rescore()
        for tf in transforms:
            tf.invert_velocity()
        score_change2 = 0
        for tf in transforms[::-1]:
            tf.step()
            score_change2 += scoring.rescore()
        # assert: rescoring yields the negative change from the first step
        assert round(score_change2 + score_change1, NDIGITS) == 0
        term_vals2 = {
            _key: _value for _t in scoring.terms for _key, _value in
            viewitems(_t.values)}
        # assert: all partial, unweighted values have been restored
        assert all([
            round(term_vals1[_key] - term_vals2[_key], NDIGITS) == 0 for
            _key in term_vals1])
        term_unwgt2 = [_t.unweighted() for _t in scoring.terms]
        # assert: all unweighted values have been restored
        assert all([
            round(_v1 - _v2, NDIGITS) == 0 for _v1, _v2 in
            zip(term_unwgt1, term_unwgt2)])
        term_wgt2 = [_t.weighted() for _t in scoring.terms]
        # assert: all weighted values have been restored
        assert all([
            round(_v1 - _v2, NDIGITS) == 0 for _v1, _v2 in
            zip(term_wgt1, term_wgt2)])
        total2 = scoring.total()
        # assert: the total score has been restored
        assert round(total1 - total2, NDIGITS) == 0
