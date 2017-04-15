# coding=utf-8
"""Mal Runtime environment with JIT Actions.

"""
from __future__ import print_function


class Flags(object):
    """Small mutable flag class

    """
    def __init__(self, div_by_zero, out_of_bounds, bad_operand):
        self.div_by_zero = div_by_zero
        self.out_of_bounds = out_of_bounds
        self.bad_operand = bad_operand

    def __str__(self):
        return "FLAGS(div_by_zero={0}, out_of_bounds={1}, bad_operand={2})"\
            .format(self.div_by_zero, self.out_of_bounds, self.bad_operand)


def no_op(_):
    """Non-operation.

    Does nothing for when no jit is needed or found.

    Returns:
        None

    """
    pass


class ActionRunner(object):
    """This is a runtime environment.

    It sets memory on instantiation and zeros the registers.

    """

    def __init__(self, actions):
        self.actions = actions
        self.memory = None
        self.halt = False
        self.flags = Flags(False, False, False)
        self.registers = [0 for _ in range(16)]
        self.program_counter = 0
        self.evaluate = {
            'MOVE': self._move,
            'MOVEI': self._movei,
            'LOAD': self._load,
            'STORE': self._store,
            'ADD': self._add,
            'INC': self._inc,
            'SUB': self._sub,
            'DEC': self._dec,
            'MUL': self._mul,
            'DIV': self._div,
            'BEQ': self._beq,
            'BLT': self._blt,
            'BGT': self._bgt,
            'BR': self._br,
            'END': self._end
        }
        self.types = {
            'END': [],
            'BR': ['L'],
            'INC': ['R'],
            'DEC': ['R'],
            'MOVE': ['R', 'R'],
            'MOVEI': ['V', 'R'],
            'LOAD': ['R', 'R'],
            'STORE': ['R', 'R'],
            'ADD': ['R', 'R', 'R'],
            'SUB': ['R', 'R', 'R'],
            'MUL': ['R', 'R', 'R'],
            'DIV': ['R', 'R', 'R'],
            'BEQ': ['R', 'R', 'L'],
            'BLT': ['R', 'R', 'L'],
            'BGT': ['R', 'R', 'L']
        }

    def _from_hex(self, reg):
        return int(reg[1:], 16)

    def _from_dec(self, val):
        return int(val[1:])

    def _create_operation(self, opcode):
        def _function(operands):
            ots = zip(operands, self.types[opcode])
            if all([op.startswith(typ) for op, typ in ots]):
                ops = [self._from_hex(op)
                       if op[0] == 'R' else self._from_dec(op)
                       for op in operands]
                self.actions.get(opcode, no_op)(ops)
                self.evaluate[opcode](ops)
            else:
                self.flags.bad_operand = True
        return _function

    def reset(self):
        """Resets the memory, registers and program counter.

        """
        self.memory = [0]*64
        self.flags = Flags(False, False, False)
        self.halt = False
        self.registers = [0]*16
        self.program_counter = 0

    def run(self, program, memory):
        """Runs an instruction set on a loaded memory and cleared register

        Args:
            program (list[list[str, list[str]]]): Instruction 'AST'.

            memory (list[int]): The memory contents used to run the program.

        Returns:
             list[int]: The memory contents

        """
        self.memory = memory
        while not any([self.halt, self.flags.div_by_zero,
                       self.flags.out_of_bounds, self.flags.bad_operand]):
            if self.program_counter >= len(program):
                self.flags.out_of_bounds = True
            else:
                opcode, operands = program[self.program_counter]
                self._create_operation(opcode)(operands)
                self.program_counter += 1

        if not any([self.flags.div_by_zero,
                    self.flags.out_of_bounds,
                    self.flags.bad_operand]):
            return self.memory
        else:
            return [self.flags.div_by_zero,
                    self.flags.out_of_bounds,
                    self.flags.bad_operand]

    def _move(self, ops):
            self.registers[ops[1]] = self.registers[ops[0]]

    def _movei(self, ops):
        self.registers[ops[1]] = ops[0]

    def _load(self, ops):
        self.registers[ops[1]] = self.memory[self.registers[ops[0]]]

    def _store(self, ops):
        self.memory[self.registers[ops[1]]] = self.registers[ops[0]]

    def _add(self, ops):
        self.registers[ops[2]] = \
            (self.registers[ops[0]] + self.registers[ops[1]]) % 64

    def _inc(self, ops):
        self.registers[ops[0]] = (self.registers[ops[0]] + 1) % 64

    def _sub(self, ops):
        self.registers[ops[2]] = \
            (self.registers[ops[2]] + 64 - self.registers[ops[1]]) % 64

    def _dec(self, ops):
        self.registers[ops[0]] = (self.registers[ops[0]] + 63) % 64

    def _mul(self, ops):
        self.registers[ops[2]] = \
            (self.registers[ops[0]] * self.registers[ops[1]]) % 64

    def _div(self, ops):
        if self.registers[ops[1]] == 0:
            self.flags.div_by_zero = True
            return  # Don't do division if reg1 is 0.
        self.registers[ops[2]] = \
            (self.registers[ops[0]] // self.registers[ops[1]]) % 64

    def _bgt(self, ops):
        if self.registers[ops[0]] > self.registers[ops[1]]:
            self.program_counter = ops[2] - 1

    def _blt(self, ops):
        if self.registers[ops[0]] < self.registers[ops[1]]:
            self.program_counter = ops[2] - 1

    def _beq(self, ops):
        if self.registers[ops[0]] == self.registers[ops[1]]:
            self.program_counter = ops[2] - 1

    def _br(self, ops):
        self.program_counter = ops[0] - 1

    def _end(self, _):
        self.halt = True
