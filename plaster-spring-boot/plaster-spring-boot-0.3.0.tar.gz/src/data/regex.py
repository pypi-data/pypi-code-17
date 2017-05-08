TYPE = '([A-Z]+)([a-zA-Z<>,]*)'

VARIABLE_NAME = '([a-z]+)([a-zA-Z_0-9]*)'

VARIABLE_DECLARATION = '\s+private\s' + TYPE + '\s' + VARIABLE_NAME + '( = .*)?;\n'

IMPORT_DECLARATION = '(import\s)((\w+\.\n*\s*)+([\w\*]+)(?=\;));'

METHOD = '\s+(public|protected|private|static) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])\n'

END_OF_FILE = '}'

CLASS = '(public|private|protected)?[\s]*(class)\s*([a-zA-Z0-9]*)\s*' \
        '(((extends) \s*([a-zA-Z0-9]*))|(implements)\s*([a-zA-Z0-9,\s]*))?' \
        '|((implements)\s*([a-zA-Z0-9,\s]*))?\s*{'
