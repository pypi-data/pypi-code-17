import os
from kcshell.kcshell import Kcshell
from keystone import *
from struct import pack
from binascii import hexlify

class Assembler(Kcshell):
    def __init__(self):
        ''' create a new assembler instance '''
        Kcshell.__init__(self)
        self.prompt = 'asm> '
        self.intro = 'Default Assembler architecture is x86 (32 bits)'
        self._ks = Ks(KS_ARCH_X86, KS_MODE_32)

    def get_ks_archs(self):
        ''' keystone assembler '''
        ks_archs = {
            'x16':     (KS_ARCH_X86,     KS_MODE_16),
            'x86':     (KS_ARCH_X86,     KS_MODE_32),
            'x64':     (KS_ARCH_X86,     KS_MODE_64),
            'arm':     (KS_ARCH_ARM,     KS_MODE_ARM),
            'arm_t':   (KS_ARCH_ARM,     KS_MODE_THUMB),
            'arm64':   (KS_ARCH_ARM64,   KS_MODE_LITTLE_ENDIAN),
            'mips32':  (KS_ARCH_MIPS,    KS_MODE_MIPS32),
            'mips64':  (KS_ARCH_MIPS,    KS_MODE_MIPS64),
            'ppc32':   (KS_ARCH_PPC,     KS_MODE_PPC32),
            'ppc64':   (KS_ARCH_PPC,     KS_MODE_PPC64),
            'hexagon': (KS_ARCH_HEXAGON, KS_MODE_BIG_ENDIAN),
            'sparc':   (KS_ARCH_SPARC,   KS_MODE_SPARC32),
            'sparc64': (KS_ARCH_SPARC,   KS_MODE_SPARC64),
            'systemz': (KS_ARCH_SYSTEMZ, KS_MODE_BIG_ENDIAN)
            }
        return ks_archs

    def help_lsarchs(self):
        print("List supported Assembler architectures.")

    def do_lsarchs(self, dummy):
        print(", ".join(self.get_ks_archs().keys()))

    def help_setarch(self):
        print("Set Assembler architecture. To list available options type 'lsarchs'.")

    def do_setarch(self, arch):
        try:
            if arch:
                ks_arch, ks_mode = self.get_ks_archs()[arch]
                self._ks = Ks(ks_arch, ks_mode)
                print('Assembler architecture is now ' + arch)
            else:
                print("Usage: setarch <arch>\nType 'lsarchs' to list all supported architectures.")
        except KsError as e:
            print("Error: %s" %e)

    def default(self, line):
        ''' if no other commands was invoked '''
        try:
            encoding, count = self._ks.asm(line)
            machine_code = ""
            for opcode in encoding:
                machine_code += "\\x" + hexlify(pack("B", opcode)).decode()
            print("\"" + machine_code + "\"")
        except KsError as e:
            print("Error: %s" %e)

