import sys

sysprint = print

def exit(stack):
    sys.exit(0)

def reset(stack):
    return []

def reverse(stack):
    stack = stack[::-1]
    return stack

def add(stack):
    a = stack.pop()
    b = stack.pop()
    try:
        stack.append(a + b)
    except TypeError:
        sysprint("Runtime Error! Shutting down your program.\n")
        sysprint("Error happened in the add function.")
        sysprint("Tried to add: {}, {}".format(a, b))
        sysprint("Apparently, this was impossible.")
        sys.exit(1)
    return stack

def take(stack):
    a = stack.pop()
    b = stack.pop()
    try:
        stack.append(a - b)
    except TypeError:
        sysprint("Runtime Error! Shutting down your program.\n")
        sysprint("Error happened in the take function.")
        sysprint("Tried to add: {}, {}".format(a, b))
        sysprint("Apparently, this was impossible.")
        sys.exit(1)
    return stack

def times(stack):
    a = stack.pop()
    b = stack.pop()
    try:
        stack.append(a * b)
    except TypeError:
        sysprint("Runtime Error! Shutting down your program.\n")
        sysprint("Error happened in the times function.")
        sysprint("Tried to add: {}, {}".format(a, b))
        sysprint("Apparently, this was impossible.")
        sys.exit(1)
    return stack

def divide(stack):
    a = stack.pop()
    b = stack.pop()
    try:
        stack.append(a / b)
    except TypeError:
        sysprint("Runtime Error! Shutting down your program.\n")
        sysprint("Error happened in the divide function.")
        sysprint("Tried to add: {}, {}".format(a, b))
        sysprint("Apparently, this was impossible.")
        sys.exit(1)
    return stack

def push(thing, stack):
    for ea in thing:
        stack.append(ea)
    return stack

def pop(stack):
    a = stack.pop()
    if hasattr(a, '__call__'):
        stack = a(stack)
    return stack

def peek(stack):
    try:
        a = stack[-1]
    except IndexError:
        a = 0
    if hasattr(a, '__call__'):
        stack = a(stack)
    return stack

def print(stack):
    for i in stack:
        if isinstance(i, str):
            bstr = str.encode(i)
            bstr = bstr.decode('unicode_escape')
            sysprint(bstr)
        else:
            sysprint(i)
    return stack
