import logging

from .stack import Stack
log = logging.getLogger('Stack')


class Memory:
    def __init__(self):
        self.stacks = []

    def new(self, stack):
        assert isinstance(stack, Stack)

        self.stacks.append(stack)
        log.debug(f"Add new stack {hex(id(stack))}")

    def destroy(self, stack):
        stack.clean()
        self.stacks.remove(stack)
        log.debug(f"Stack {hex(id(stack))} destroyed")

    def clean(self):
        for stack in self.stacks:
            stack.clean()
            del stack
