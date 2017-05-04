from boolparser import BoolParser, EvaluateVariable


class ncar(object):
    def __init__(self,var):
        self.var = var
        return
    def __ge__(self, num):
        return self.var>=num
    def __le__(self, num):
        return self.var<=num
    def __gt__(self, num):
        return self.var>num
    def __lt__(self, num):
        return self.var<num
    
def define_class(nc):
    class ev_nc(EvaluateVariable):
       def eval(self):
            if self.value in nc.variables:
                return ncar(nc.variables[self.value][:])
            elif self.value in nc.dimensions:
                return ncar(nc.dimensions[self.value][:])
            else:
                raise NameError("Not a variable: {0}".format(self.value))
                return self.value
    return ev_nc


def boolfilter(nc, condition):
    nceval = define_class(nc)
    bp = BoolParser(nceval)
    return bp.parse(condition)
    
