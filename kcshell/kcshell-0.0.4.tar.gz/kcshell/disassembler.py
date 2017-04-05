import os
from kcshell.kcshell import Kcshell
from capstone import *
from binascii import unhexlify

class Disassembler(Kcshell):
    def __init__(self):
        ''' creates a new disassembler instance '''
        Kcshell.__init__(self)
        self.prompt = 'disasm> '
        self.intro = 'Default Disassembler architecture is x86 (32 bits)'
        self._cs = Cs(CS_ARCH_X86, CS_MODE_32)
        self.base_address = 0x00400000

    def get_cs_archs(self):
        ''' capstone disassembler '''
        cs_archs = {
            'x16':     (CS_ARCH_X86,     CS_MODE_16),
            'x86':     (CS_ARCH_X86,     CS_MODE_32),
            'x64':     (CS_ARCH_X86,     CS_MODE_64),
            'arm':     (CS_ARCH_ARM,     CS_MODE_ARM),
            'arm_t':   (CS_ARCH_ARM,     CS_MODE_THUMB),
            'arm64':   (CS_ARCH_ARM64,   CS_MODE_LITTLE_ENDIAN),
            'mips32':  (CS_ARCH_MIPS,    CS_MODE_MIPS32),
            'mips64':  (CS_ARCH_MIPS,    CS_MODE_MIPS64),
            }
        return cs_archs

    def cleanup(self, input_str):
        input_str = input_str.replace(" ", "")
        input_str = input_str.replace("\\x", "")
        return input_str.replace("0x", "")

    def help_lsarchs(self):
        print("List supported Disassembler architectures.")

    def do_lsarchs(self, dummy):
        print(", ".join(self.get_cs_archs().keys()))

    def help_setarch(self):
        print("Set Disassembler architecture. To list available options type 'lsarchs'.")

    def do_setarch(self, arch):
        try:
            if arch:            
                cs_arch, cs_mode = self.get_cs_archs()[arch]
                self._cs = Cs(cs_arch, cs_mode)
                print('Disassembler architecture is now ' + arch)
            else:
                print("Usage: setarch <arch>\nType 'lsarchs' to list all supported architectures.")
        except CsError as e:
            print("Error: %s" %e)

    def default(self, user_input):
        ''' if no other command was invoked '''
        try:
            for i in self._cs.disasm(unhexlify(self.cleanup(user_input)), self.base_address):
                print("0x%08x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
        except CsError as e:
            print("Error: %s" %e)

