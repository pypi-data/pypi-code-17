import sys
from cmd import Cmd
from kcshell import config

class Kcshell(Cmd):
    ''' Common Assembler and Disassembler commands '''
    def __init__(self):
        Cmd.__init__(self)

    def cmdloop(self, intro=None):
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            ''' catch ctrl + c '''
            raise SystemExit

    def help_quit(self):
        print("Quits the application.")

    def do_quit(self, dummy_args):
        raise SystemExit

    def help_exit(self):
        print("Quits the application.")

    def do_exit(self, dummy):
        raise SystemExit

    def help_EOF(self):
        print("Quits the application.")

    def do_EOF(self, line):
        raise SystemExit

    def help_lsmodes(self):
        print("Lists current operational modes available.")

    def do_lsmodes(self, dummy):
        print(", ".join(config.get_op_modes().keys()))

    def help_setmode(self):
        print("Sets 'kcshell' operational mode. For available options run 'lsmodes'.")

    def do_setmode(self, arg):
        ''' shift from ASM to DISASM '''
        op_modes = config.get_op_modes()
        if arg in op_modes:
            op_mode = op_modes[arg]
            op_mode.cmdloop()
        else:
            print("Error: unknown operational mode, please use 'help setmode'.")

