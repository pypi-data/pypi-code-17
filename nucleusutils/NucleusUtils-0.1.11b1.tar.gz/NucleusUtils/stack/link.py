import logging

log = logging.getLogger('Stack')


class MemoryLink:
    def __init__(self, stack, pos, name):
        self.stack = stack
        self.pos = pos
        self.name = name
        log.debug(f"Set '{name}' at {stack}:{pos}")

    def get(self):
        log.debug(f"Get '{self.name}' from {self.stack}:{self.pos}")
        return self.stack.get(self.pos)

    def destroy(self):
        return self.stack.pop(self.pos)

    def __str__(self):
        return f"[&{self.pos} {self.name}]"
