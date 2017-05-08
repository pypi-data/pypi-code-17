from inspect import isroutine


class SingleDelegated(object):
    delegate = None

    def __init__(self, delegate=None):
        self.delegate = delegate

    def __getattr__(self, item):
        return getattr(self.delegate, item)

    def __setattr__(self, name, value):
        if self.delegate is None or name in self.__dict__:
            self.__dict__[name] = value
        else:
            setattr(self.delegate, name, value)


class MultiDelegated(object):
    __delegates = None

    @staticmethod
    def __default_predicate(x):
        return x

    def __get_predicate(self, name):
        return self.__predicates.get(name, self.__default_predicate)

    def __init__(self, *delegates):
        self.__predicates = dict()
        self.__delegates = delegates

    @property
    def delegates(self):
        return self.__delegates

    def set_default_predicate(self, predicate):
        self.__default_predicate = predicate

    def set_predicate(self, name, predicate):
        self.__predicates[name] = predicate

    def __routine_attr(self, name, attrs):
        def __call_attr(*args, **kwargs):
            results = []
            for attr in attrs:
                result = attr(*args, **kwargs)
                results.append(result)
            return self.__get_predicate(name)(results)
        return __call_attr

    def __getattr__(self, name):
        non_routine_attrs = []
        routine_attrs = []
        for delegate in self.__delegates:
            attr = getattr(delegate, name)
            attrs = routine_attrs if isroutine(attr) else non_routine_attrs
            attrs.append(attr)

        if non_routine_attrs:
            return self.__get_predicate(name)(non_routine_attrs + routine_attrs)

        return self.__routine_attr(name, routine_attrs)

    def __setattr__(self, name, value):
        if self.__delegates is None or name in self.__dict__:
            self.__dict__[name] = value
        else:
            for delegate in self.__delegates:
                setattr(delegate, name, value)


if __name__ == '__main__':

    class A(object):
        value = 'A.value'

        def foo(self, arg):
            return 'A.foo', self.__class__

        def bar(self, arg):
            return 'A.bar', self.__class__

        def xyz(self, arg):
            return 'A.xyz', self.__class__

        @property
        def delegated_property(self):
            return self.value

        @delegated_property.setter
        def delegated_property(self, value):
            self.value = value


    class B(SingleDelegated):
        value = 'B.value'

        def bar(self, arg):
            return 'B.bar', self.__class__


    class C(SingleDelegated):
        def foo(self, arg):
            return 'C.foo', self.__class__

        def xyz(self, arg):
            return 'C.xyz', self.__class__


    class D(MultiDelegated):
        def foo(self, arg):
            return 'D.foo', self.__class__

    # Test SingleDelegated callables
    assert A().foo('arg') == ('A.foo', A)
    assert A().xyz('arg') == ('A.xyz', A)
    assert B().bar('arg') == ('B.bar', B)
    assert B(A()).foo('arg') == ('A.foo', A)
    assert B(A()).bar('arg') == ('B.bar', B)
    assert B(A()).xyz('arg') == ('A.xyz', A)
    assert C().foo('arg') == ('C.foo', C)
    assert C(A()).foo('arg') == ('C.foo', C)
    assert C(A()).xyz('arg') == ('C.xyz', C)
    assert C(B()).foo('arg') == ('C.foo', C)
    assert C(B()).bar('arg') == ('B.bar', B)
    assert C(B(A())).foo('arg') == ('C.foo', C)
    assert C(B(A())).bar('arg') == ('B.bar', B)
    assert C(B(A())).xyz('arg') == ('C.xyz', C)

    # Test SingleDelegated data-members
    assert A().value == A.value
    assert B(A()).value == B.value
    assert C(A()).value == A.value
    assert C(B()).value == B.value
    assert C(B(A())).value == B.value

    # Test SingleDelegated properties
    b = B(A())
    b.delegated_property = 'another value'
    assert b.delegate.delegated_property == 'another value'

    # Test MultiDelegated callables
    assert D().foo('arg') == ('D.foo', D)

    assert D(A()).foo('arg') == ('D.foo', D)
    assert D(A()).xyz('arg') == [('A.xyz', A)]

    assert D(B()).foo('arg') == ('D.foo', D)
    assert D(B()).bar('arg') == [('B.bar', B)]

    assert D(C()).foo('arg') == ('D.foo', D)

    assert D(C(B())).foo('arg') == ('D.foo', D)
    assert D(C(B())).bar('arg') == [('B.bar', B)]

    assert D(B(A())).foo('arg') == ('D.foo', D)
    assert D(B(A())).bar('arg') == [('B.bar', B)]
    assert D(B(A())).xyz('arg') == [('A.xyz', A)]

    assert D(A(), B()).foo('arg') == ('D.foo', D)

    assert D(A(), C()).foo('arg') == ('D.foo', D)
    assert D(A(), C()).xyz('arg') == [('A.xyz', A), ('C.xyz', C)]

    assert D(A(), B(A())).foo('arg') == ('D.foo', D)
    assert D(A(), B(A())).xyz('arg') == [('A.xyz', A), ('A.xyz', A)]

    assert D(B(A()), B()).bar('arg') == [('B.bar', B), ('B.bar', B)]

    assert D(A(), B(), C()).foo('arg') == ('D.foo', D)

    assert D(A(), B(A()), C(A())).foo('arg') == ('D.foo', D)
    assert D(A(), B(A()), C(A())).xyz('arg') == [('A.xyz', A), ('A.xyz', A), ('C.xyz', C)]

    assert D(B(A()), B(), C(B())).foo('arg') == ('D.foo', D)
    assert D(B(A()), B(), C(B())).bar('arg') == [('B.bar', B), ('B.bar', B), ('B.bar', B)]
    assert D(B(A()), B(A()), C(B())).xyz('arg') == [('A.xyz', A), ('A.xyz', A), ('C.xyz', C)]

    # Test MultiDelegated properties
    d = D(A())
    d.delegated_property = 'another value'
    assert d.delegated_property  == ['another value']
    assert d.delegates[0].delegated_property  == 'another value'
