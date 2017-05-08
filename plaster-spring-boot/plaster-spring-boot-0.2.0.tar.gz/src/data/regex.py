TYPE = '([A-Z]+)([a-zA-Z<>,]*)'

VARIABLE_NAME = '([a-z]+)([a-zA-Z_0-9]*)'

VARIABLE_DECLARATION = '\s+private\s' + TYPE + '\s' + VARIABLE_NAME + '( = .*)?;\n'

METHOD = '\s+(public|protected|private|static) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])\n'

END_OF_FILE = '}'
