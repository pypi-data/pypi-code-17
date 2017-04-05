from kcshell.assembler import Assembler
from kcshell.disassembler import Disassembler

def get_op_modes():
    OP_MODES = {
        'asm' : Assembler(),
        'disasm' : Disassembler()
    }
    return OP_MODES

def get_default_op_mode():
    return 'asm'

