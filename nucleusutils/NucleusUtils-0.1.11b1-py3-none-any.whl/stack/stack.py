from .link import MemoryLink


class Stack:
    def __init__(self):
        from . import memory
        memory.new(self)
        self.__stack = {}

    def add(self, obj):
        pos = hex(id(obj))
        self.__stack[pos] = obj

        if hasattr(obj, 'get_reference'):
            if hasattr(obj, 'get_full_reference') and not hasattr(obj, '__name__'):
                name = obj.get_full_reference()
            else:
                name = obj.get_reference()
        elif hasattr(obj, '__name__'):
            name = obj.__name__
        else:
            print('__class__.__name__')
            name = obj.__class__.__name__

        print(name)
        return MemoryLink(self, pos, name)

    def get(self, pos):
        if pos not in self.__stack:
            raise MemoryError
        return self.__stack[pos]

    def pop(self, pos):
        if pos not in self.__stack:
            raise MemoryError
        return self.__stack.pop(pos)

    def check(self, pos):
        return pos in self.__stack

    def clean(self):
        for element in self.__stack:
            del element
