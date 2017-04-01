# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines utility classes and functions.
"""

import six
from io import open
import os
import tempfile
from subprocess import Popen, PIPE

import numpy as np

try:
    import pybel as pb
except ImportError:
    pb = None
from pymatgen import Molecule
from pymatgen.core.operations import SymmOp
from pymatgen.util.coord_utils import get_angle
from pymatgen.io.babel import BabelMolAdaptor

from monty.os.path import which
from monty.dev import requires
from monty.tempfile import ScratchDir

__author__ = 'Kiran Mathew, Brandon Wood, Michael Humbert'
__email__ = 'kmathew@lbl.gov'


class Polymer(object):
    """
    Generate polymer chain via Random walk. At each position there are
    a total of 5 possible moves(excluding the previous direction).
    """
    def __init__(self, start_monomer, s_head, s_tail,
                 monomer, head, tail,
                 end_monomer, e_head, e_tail,
                 n_units, link_distance=1.0, linear_chain=False):
        """
        Args:
            start_monomer (Molecule): Starting molecule
            s_head (int): starting atom index of the start_monomer molecule
            s_tail (int): tail atom index of the start_monomer
            monomer (Molecule): The monomer
            head (int): index of the atom in the monomer that forms the head
            tail (int): tail atom index. monomers will be connected from
                tail to head
            end_monomer (Molecule): Terminal molecule
            e_head (int): starting atom index of the end_monomer molecule
            e_tail (int): tail atom index of the end_monomer
            n_units (int): number of monomer units excluding the start and
                terminal molecules
            link_distance (float): distance between consecutive monomers
            linear_chain (bool): linear or random walk polymer chain
        """
        self.start = s_head
        self.end = s_tail
        self.monomer = monomer
        self.n_units = n_units
        self.link_distance = link_distance
        self.linear_chain = linear_chain
        # translate monomers so that head atom is at the origin
        start_monomer.translate_sites(range(len(start_monomer)),
                                      - monomer.cart_coords[s_head])
        monomer.translate_sites(range(len(monomer)),
                                - monomer.cart_coords[head])
        end_monomer.translate_sites(range(len(end_monomer)),
                                    - monomer.cart_coords[e_head])
        self.mon_vector = monomer.cart_coords[tail] - monomer.cart_coords[head]
        self.moves = {1: [1, 0, 0],
                      2: [0, 1, 0],
                      3: [0, 0, 1],
                      4: [-1, 0, 0],
                      5: [0, -1, 0],
                      6: [0, 0, -1]}
        self.prev_move = 1
        # places the start monomer at the beginning of the chain
        self.molecule = start_monomer.copy()
        self.length = 1
        # create the chain
        self._create(self.monomer, self.mon_vector)
        # terminate the chain with the end_monomer
        self.n_units += 1
        end_mon_vector = end_monomer.cart_coords[e_tail] - \
                         end_monomer.cart_coords[e_head]
        self._create(end_monomer, end_mon_vector)

    def _create(self, monomer, mon_vector):
        """
        create the polymer from the monomer

        Args:
            monomer (Molecule)
            mon_vector (numpy.array): molecule vector that starts from the
                start atom index to the end atom index
        """
        while self.length != (self.n_units-1):
            if self.linear_chain:
                move_direction = np.array(mon_vector) / np.linalg.norm(mon_vector)
            else:
                move_direction = self._next_move_direction()
            self._add_monomer(monomer.copy(), mon_vector, move_direction)

    def _next_move_direction(self):
        """
        pick a move at random from the list of moves
        """
        nmoves = len(self.moves)
        move = np.random.randint(1, nmoves+1)
        while self.prev_move == (move + 3) % nmoves:
            move = np.random.randint(1, nmoves+1)
        self.prev_move = move
        return np.array(self.moves[move])

    def _align_monomer(self, monomer, mon_vector, move_direction):
        """
        rotate the monomer so that it is aligned along the move direction

        Args:
            monomer (Molecule)
            mon_vector (numpy.array): molecule vector that starts from the
                start atom index to the end atom index
            move_direction (numpy.array): the direction of the polymer chain
                extension
        """
        axis = np.cross(mon_vector, move_direction)
        origin = monomer[self.start].coords
        angle = get_angle(mon_vector, move_direction)
        op = SymmOp.from_origin_axis_angle(origin, axis, angle)
        monomer.apply_operation(op)

    def _add_monomer(self, monomer, mon_vector, move_direction):
        """
        extend the polymer molecule by adding a monomer along mon_vector direction

        Args:
            monomer (Molecule): monomer molecule
            mon_vector (numpy.array): monomer vector that points from head to tail.
            move_direction (numpy.array): direction along which the monomer
                will be positioned
        """
        translate_by = self.molecule.cart_coords[self.end] + \
                       self.link_distance * move_direction
        monomer.translate_sites(range(len(monomer)), translate_by)
        if not self.linear_chain:
            self._align_monomer(monomer, mon_vector, move_direction)
        # add monomer if there are no crossings
        does_cross = False
        for i, site in enumerate(monomer):
            try:
                self.molecule.append(site.specie, site.coords,
                                     properties=site.properties)
            except:
                does_cross = True
                polymer_length = len(self.molecule)
                self.molecule.remove_sites(
                    range(polymer_length - i, polymer_length))
                break
        if not does_cross:
            self.length += 1
            self.end += len(self.monomer)


class PackmolRunner(object):
    """
    Wrapper for the Packmol software that can be used to pack various types of
    molecules into a one single unit.
    """

    @requires(which('packmol'),
              "PackmolRunner requires the executable 'packmol' to be in "
              "the path. Please download packmol from "
              "https://github.com/leandromartinez98/packmol "
              "and follow the instructions in the README to compile. "
              "Don't forget to add the packmol binary to your path")
    def __init__(self, mols, param_list, input_file="pack.inp",
                 tolerance=2.0, filetype="xyz",
                 control_params={"maxit": 20, "nloop": 600},
                 auto_box=True, output_file="packed.xyz"):
        """
        Args:
              mols:
                   list of Molecules to pack
              input_file:
                        name of the packmol input file
              tolerance:
                        min distance between the atoms
              filetype:
                       input/output structure file type
              control_params:
                           packmol control parameters dictionary. Basically
                           all parameters other than structure/atoms
              param_list:
                    list of parameters containing dicts for each molecule
              auto_box:
                    put the molecule assembly in a box
              output_file:
                    output file name. The extension will be adjusted
                    according to the filetype
        """
        self.mols = mols
        self.param_list = param_list
        self.input_file = input_file
        self.boxit = auto_box
        self.control_params = control_params
        if not self.control_params.get("tolerance"):
            self.control_params["tolerance"] = tolerance
        if not self.control_params.get("filetype"):
            self.control_params["filetype"] = filetype
        if not self.control_params.get("output"):
            self.control_params["output"] = "{}.{}".format(
                output_file.split(".")[0], self.control_params["filetype"])
        if self.boxit:
            self._set_box()

    def _format_param_val(self, param_val):
        """
        Internal method to format values in the packmol parameter dictionaries

        Args:
              param_val:
                   Some object to turn into String

        Returns:
               string representation of the object
        """
        if isinstance(param_val, list):
            return ' '.join(str(x) for x in param_val)
        else:
            return str(param_val)

    def _set_box(self):
        """
        Set the box size for the molecular assembly
        """
        net_volume = 0.0
        for idx, mol in enumerate(self.mols):
            length = max([np.max(mol.cart_coords[:, i])-np.min(mol.cart_coords[:, i])
                           for i in range(3)]) + 2.0
            net_volume += (length**3.0) * float(self.param_list[idx]['number'])
        length = net_volume**(1.0/3.0)
        for idx, mol in enumerate(self.mols):
            self.param_list[idx]['inside box'] = '0.0 0.0 0.0 {} {} {}'.format(
                length, length, length)

    def _write_input(self, input_dir="."):
        """
        Write the packmol input file to the input directory.

        Args:
            input_dir (string): path to the input directory
        """
        with open(os.path.join(input_dir, self.input_file), 'wt', encoding="utf-8") as inp:
            for k, v in six.iteritems(self.control_params):
                inp.write('{} {}\n'.format(k, self._format_param_val(v)))
            # write the structures of the constituent molecules to file and set
            # the molecule id and the corresponding filename in the packmol
            # input file.
            for idx, mol in enumerate(self.mols):
                a = BabelMolAdaptor(mol)
                pm = pb.Molecule(a.openbabel_mol)
                filename = os.path.join(
                    input_dir, '{}.{}'.format(
                        idx, self.control_params["filetype"])).encode("ascii")
                pm.write(self.control_params["filetype"], filename=filename,
                         overwrite=True)
                inp.write("\n")
                inp.write(
                    "structure {}.{}\n".format(
                        os.path.join(input_dir, str(idx)),
                        self.control_params["filetype"]))
                for k, v in six.iteritems(self.param_list[idx]):
                    inp.write('  {} {}\n'.format(k, self._format_param_val(v)))
                inp.write('end structure\n')

    def run(self, copy_to_current_on_exit=False):
        """
        Write the input file to the scratch directory, run packmol and return
        the packed molecule.

        Args:
            copy_to_current_on_exit (bool): Whether or not to copy the packmol
                input/output files from the scratch directory to the current
                directory.

        Returns:
                Molecule object
        """
        scratch = tempfile.gettempdir()
        with ScratchDir(scratch, copy_to_current_on_exit=copy_to_current_on_exit) as scratch_dir:
            self._write_input(input_dir=scratch_dir)
            packmol_bin = ['packmol']
            packmol_input = open(os.path.join(scratch_dir, self.input_file), 'r')
            p = Popen(packmol_bin, stdin=packmol_input, stdout=PIPE, stderr=PIPE)
            p.wait()
            (stdout, stderr) = p.communicate()
            output_file = os.path.join(scratch_dir, self.control_params["output"])
            if os.path.isfile(output_file):
                packed_mol = BabelMolAdaptor.from_file(output_file)
                print("packed molecule written to {}".format(
                    self.control_params["output"]))
                return packed_mol.pymatgen_mol
            else:
                print("Packmol execution failed")
                print(stdout, stderr)
                return None


class LammpsRunner(object):
    def __init__(self, dict_input, input_filename="lammps.in", bin="lammps"):
        """
        LAMMPS wrapper

        Args:
            dict_input (DictLammpsInput): lammps input object
            input_filename (string): input file name
            bin (string): command to run, excluding the input file name
        """
        self.lammps_bin = bin.split()
        if not which(self.lammps_bin[-1]):
            raise RuntimeError(
                "LammpsRunner requires the executable {} to be in the path. "
                "Please download and install LAMMPS from " \
                "http://lammps.sandia.gov. "
                "Don't forget to add the binary to your path".format(self.lammps_bin[-1]))
        self.dict_input = dict_input
        self.input_filename = input_filename

    def run(self):
        """
        Write the input/data files and run LAMMPS.
        """
        self.dict_input.write_input(self.input_filename)
        print("Input file: {}".format(self.input_filename))
        lammps_cmd = self.lammps_bin + ['-in', self.input_filename]
        print("Running: {}".format(" ".join(lammps_cmd)))
        p = Popen(lammps_cmd, stdout=PIPE, stderr=PIPE)
        p.wait()
        (stdout, stderr) = p.communicate()
        print("Done")
        print(stdout, stderr)


if __name__ == '__main__':
    ethanol_coords = [[0.00720, -0.56870, 0.00000],
                      [-1.28540, 0.24990, 0.00000],
                      [1.13040, 0.31470, 0.00000],
                      [0.03920, -1.19720, 0.89000],
                      [0.03920, -1.19720, -0.89000],
                      [-1.31750, 0.87840, 0.89000],
                      [-1.31750, 0.87840, -0.89000],
                      [-2.14220, -0.42390, -0.00000],
                      [1.98570, -0.13650, -0.00000]]
    ethanol = Molecule(["C", "C", "O", "H", "H", "H", "H", "H", "H"],
                       ethanol_coords)
    water_coords = [[9.626, 6.787, 12.673],
                    [9.626, 8.420, 12.673],
                    [10.203, 7.604, 12.673]]
    water = Molecule(["H", "H", "O"], water_coords)
    pmr = PackmolRunner([ethanol, water],
                        [{"number": 1, "fixed": [0, 0, 0, 0, 0, 0],
                          "centerofmass": ""},
                         {"number": 15, "inside sphere": [0, 0, 0, 5]}],
                        input_file="packmol_input.inp", tolerance=2.0,
                        filetype="xyz",
                        control_params={"nloop": 1000},
                        auto_box=False, output_file="cocktail.xyz")
    s = pmr.run()
