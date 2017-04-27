def prettyPrint(clazz):
    
    def __prettyPrint__(obj):
        propsStr = ['%s=%s' %(name, value) for name, value in obj.__dict__.iteritems()]
        return clazz.__name__ + '[' + ', '.join(propsStr) + ']'
    
    clazz.__repr__ = __prettyPrint__
    return clazz

'''
@prettyPrint
class A(object):
    def __init__(self, a = 42):
        self.a = a

a = A()
print a
print a.a
'''