from kaeru_parser import Compiler, Printer
from pre_kaeru_parser import add_numbers
import sys

filename = sys.argv[1]
text = add_numbers(filename)
compiler = Compiler()
printer = Printer()

compiler.compile(text)
entity_table = compiler.entity_table
print(entity_table['Home'].num)
printer.show_list(entity_table)
