import operator
import sys
import traceback
from pprint import pprint
import random
import collections


def is_iterable(item):
    return isinstance(item, collections.Iterable) and not isinstance(item, str)

def is_not_iterable(item):
    return not isinstance(item, collections.Iterable)

def flatten(x):
    if isinstance(x, collections.Iterable) and not isinstance(x, str):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

def hashify(item):
    if is_iterable(item):
        return tuple([hashify(i) for i in item])
    else:
        return item

def brokify(item):
    if is_iterable(item):
        return Broken(*[brokify(i) for i in item])
    else:
        return item

class Broken(list):

    for i in ['mul', 'add', 'sub', 'mod', 'div', 'pow']:
        exec("def __{operation}__(self,operand): return self.op_check(operand)".format(operation=i))

    for i in ['len', 'sum', 'max', 'min', 'str', 'int']:
        exec('@property\ndef {function}(self): return {function}(self)'.format(function=i))

    del i

    def __init__(self, *args):
        super(Broken, self).__init__([])
        self.__dict__['set'] = set()

        if is_iterable(args):
            self[:] += args
        else:
            super(Broken, self).append(args)

        self.__dict__['set'] = set(hashify(self[:]))
        # else:
        #    pass# self.append(*args)


    def op_transform(self, operand):
        func_name = traceback.extract_stack()[-3][2][2:-2]  # eg mul add ect
        self[:] = [eval("operator.{func_name}(i,{operand})".format(func_name=func_name, operand=operand)) for i in self]

    def op_list(self, l):
        func_name = traceback.extract_stack()[-3][2][2:-2]
        self[:] = [eval("operator.{func_name}(a,b)".format(func_name=func_name)) for a, b in zip(self, l)]

    def op_check(self, operand):
        if isinstance(operand, list):
            self.op_list(operand)
        elif isinstance(operand, int):
            self.op_transform(operand)
        return self

    def __contains__(self, item):
        return item in self.set

    def append(self, *args):
        self[:] += brokify(args)
        for i in args: self.set.add(i if isinstance(i, collections.Hashable) else hashify(i))
        return self

    def __and__(self, item):
        return list(self.set & set(item))

    def __or__(self, item):
        return list(self.set | set(item))

    @property
    def shuffle(self):
        random.shuffle(self)
        return self

    def __int__(self):
        return int(''.join(str(i) for i in self))

    def unique(self):
        self[:] = list(self.set)
        return self

    def difference(self, item):
        return list(self.set - set(item))

    def symmetric_difference(self, item):
        return list(self.set ^ set(item))

    @property
    def clear(self):
        self[:] = []
        self.__dict__['set'] = set()
        return self

    @property
    def sort(self):
        self[:] = sorted(self)
        return self


    def add(self, item):
        if hashify(item) not in self.set:
            self.append(item)

        return self

    def remove(self, item):
        for i in self:
            if i == item:
                a = list(self[:])
                a.remove(i)
                if i not in self:
                    self.set.remove(i)
                self[:] = a
                break
        return self

    def remove_all(self, item):
        while item in self.set:
            self.remove(item)
        return self


    def _get_index(self,item):

        if self.flen > 3:
            for i,j in enumerate(self):
                if hasattr(j, '__iter__') and j[0] == item:
                        temp = self[i][1:][0]
                        if is_not_iterable(temp):
                            self.__dict__['index_num'] = i
                            pass
                        else:
                            self.__dict__['index_num'] = i
                            pass
        elif self.flen <= 3 and not self.flen == 2  and self.len == 2:
            temp = self[1:][0]
            self.__dict__['index_num'] = self.index(temp)
            pass
        elif self.flen <= 3 and not self.flen == 2:
            temp = self[1:][0]
            self.__dict__['index_num'] = self.index(temp)
            pass
        elif self.flen == 2:
            pass

    def __getattr__(self, item):

        if self.flen > 3:
            for i,j in enumerate(self):
                if hasattr(j, '__iter__') and j[0] == item:
                        temp = self[i][1:][0]
                        if is_not_iterable(temp):
                            self.__dict__['index_num'] = i
                            return Broken(temp)[0]
                        else:
                            self.__dict__['index_num'] = i
                            return Broken(*temp)
        elif self.flen <= 3 and not self.flen == 2  and self.len == 2:
            temp = self[1:][0]
            self.__dict__['index_num'] = self.index(temp)
            return Broken(*temp)
        elif self.flen <= 3 and not self.flen == 2:
            temp = self[1:][0]
            self.__dict__['index_num'] = self.index(temp)
            return Broken(*temp)
        elif self.flen == 2:
            return Broken(self[1:][0])[0]




    def __getitem__(self, item):
        #super(Broken, self).__getitem__(item)
        if isinstance(item, int):
            return self[:][item]
        elif isinstance(item,str):
            for i, j in enumerate(self):

                if self.len == 2 and isinstance(j, str):
                    return brokify(self[:][1])
                elif is_iterable(j):
                    if isinstance(j[0], str):
                        return brokify(self[:][i][1])

    @property
    def flatten(self):
        if is_iterable(self):
            return Broken(*[a for i in self for a in flatten(i)])
        else:
            return self

    @property
    def flen(self):
        return self.flatten.len

    def __setattr__(self, name, value):
        try:
            #super(Broken, self).__setattr__(name, value)
            #self.__dict__[name] = value
            self.__dict__[name] = brokify(value)
            self._get_index(name)
            if is_iterable(value):
                # print self.index_num
                # print  self[self.index_num]
                self[self.index_num][1] = brokify(value)
            else:
                # print self.index_num
                # print  self[self.index_num]
                self[self.index_num][1] = brokify(value)
        except:
            pass



if __name__ == '__main__':
    a = Broken(1, 2, 3, ['ey', ['i', ['ju7', 5]]])