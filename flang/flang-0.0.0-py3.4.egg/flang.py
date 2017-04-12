#inbuilt
import pprint
import argparse
import sys

#library
import stdlib

def tokenise(str):
    """Convert a program into an untyped syntax tree"""
    tokens = []
    for line in str.split("\n"):
        if line:
            tokens.append(line.split(" "))
    return tokens

def parse(tokens):
    """Turn an untyped syntax tree into a viable program for evaluation"""
    tree = []
    errors = []
    env = get_env()
    for line, token in enumerate(tokens):
        if token:
            if isinstance(token, list):
                tree.append([])
                is_string = False
                whole_string = []
                isComment = False
                for word, i in enumerate(token):
                    if not isComment:
                        if i:
                            if i == ';':
                                isComment = True
                                continue
                            if is_string:
                                whole_string.append(i)
                                if word + 1 == len(token):
                                    tree[-1].append(' '.join(whole_string))
                                    is_string = False
                                    whole_string = []
                                continue
                            if word == 0:
                                if i in env.keys():
                                    pass
                                else:
                                    errors.append("Flang thinks that the function called here, isn't a function: \t{}\nThis happens on line {}\nThe whole line in your program looks like: \n\t{}".format(i, line + 1, ' '.join(token)))
                            if word == 1:
                                if i[0] == 's':
                                    is_string = True
                                    whole_string.append(i[1:])
                                    if word + 1 == len(token):
                                        tree[-1].append(' '.join(whole_string))
                                        is_string = False
                                        whole_string = []
                                    continue
                            if is_num(i):
                                tree[-1].append(make_num(i, is_num(i)))
                            else:
                                try:
                                    tree[-1].append(env[i.lower()])
                                except KeyError:
                                    errors.append('Flang isn\'t sure what this means: \t{}\nFound on line {}, word number {}, of your program.\nThat entire line from your program looks like: \n\n\t{}'.format(i, line + 1, word + 1, ' '.join(token)))
    tree = [x for x in tree if x]
    return (tree, errors)

def eval(parseTuple, stack=[]):
    """Evaluate a fully typed and ready program tree"""
    if parseTuple[1]:
        print("Errors found! Program did not run.\n")
        for e in parseTuple[1]:
            print('Error: {}\n'.format(e))
    else:
        for ea in parseTuple[0]:
            if len(ea) > 1:
                try:
                    stack = ea[0](stack, ea[1:])
                except TypeError:
                    print("Runtime Error! Shutting down your program.\n")
                    print("Error occured with this command: \t{}".format(ea[0]))
                    print("At a guess, {} got too many, or too few arguments. (The other words on the same line.)\nIt's also possible that {} isn't a function.".format(ea[0], ea[0]))
                    print("You gave these arguments: {}\n".format(ea[1:]))
                    sys.exit(1)
            else:
                try:
                    stack = ea[0](stack)
                except TypeError:
                    print("Runtime Error! Shutting down your program.\n")
                    print("Error occured with this command: \t{}".format(ea[0]))
                    print("At a guess, this isn't actually a function, but you tried to use it as one. Try putting a command at the start of the line.")
                    print("The other possibility, is a problem with Flang itself. Please let me know what went wrong, if you think this is the case!")
                    sys.exit(1)
    return stack

def get_env():
    """Build the base environment"""
    env = {}
    env['exit'] = stdlib.exit
    env['reset'] = stdlib.reset
    env['reverse'] = stdlib.reverse
    env['push'] = stdlib.push
    env['add'] = stdlib.add
    env['take'] = stdlib.take
    env['times'] = stdlib.times
    env['divide'] = stdlib.divide
    env['print'] = stdlib.print
    env['pop'] = stdlib.pop
    env['peek'] = stdlib.peek
    return env

def is_num(token):
    """Determine if something is a number, and if so, what kind"""
    if token.isdigit():
        return 'int'
    elif token.startswith('-') and token[1:].isdigit():
        return 'neg int'
    elif '.' in token:
        if len(token.split('.')) == 2 and token.split('.')[0].isdigit() and token.split('.')[1].isidigit():
            return 'float'
        elif len(token.split('.')) == 2 and token.startswith('-') and token[1:].split('.')[0].isdigit() and token[1:].split('.')[1].isdigit():
            return 'neg float'
        else:
            return False
    else:
        return False

def make_num(num, kind):
    """Turn a string of a number, into a number, using a provided type. See is_num"""
    if kind == 'int':
        return int(num)
    elif kind == 'neg int':
        return int(num)
    elif kind == 'float':
        return float(num)
    elif kind == 'neg float':
        return float(num)
    else:
        assert TypeError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The name of a file containing a Flang program, or the word repl for an interactive prompt.")
    args = parser.parse_args()
    if args.file.lower() != 'repl':
        with open(args.file, 'r') as openFile:
            data = openFile.read()
        eval(parse(tokenise(data)))
    else:
        stack = []
        while True:
            data = input(": ")
            stack = eval(parse(tokenise(data)), stack = stack)

if __name__ == "__main__":
    main()
