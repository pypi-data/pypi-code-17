#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sourcerer
----------------------------------

Tests for `sourcerer` module.
"""

from sourcerer import Statement, Name, Str, Num, FunctionDef, DecoratorDef, ClassDef, Attribute, Call, Document, Return, Docstring, Assignment
from inspect import isgenerator
import pytest

# Test Base


class TestStatment():

    def test_defaults(self):
        s = Statement()
        assert s.code == ''
        assert s.scope == []
        assert s.whitespace == '    '
        assert s.line_ending == ''

    def test_add_child(self):
        s = Statement()
        s2 = Statement()
        s.add_child(s2)
        assert s2 in s.scope

    def test_add_children(self):
        s = Statement()
        s21 = Statement()
        s22 = Statement()
        s2 = [s21, s22]
        s3 = Statement()
        s.add_children([s2, s3])
        assert s.scope[0] is s21
        assert s.scope[1] is s22
        assert s.scope[2] is s3

    def test_create_lineage(self):
        s = Statement()
        s21 = Statement()
        s22 = Statement()
        s2 = [s21, s22]
        s3 = Statement()
        s.create_lineage([s2, s3])
        assert s.scope[0] is s21
        assert s.scope[1] is s22
        child = s.scope[1]
        assert child.scope[0] is s3

    def test_from_parent(self):
        s = Statement()
        s2 = Statement()
        s2.from_parent(s)
        assert s2 in s.scope

    def test_from_lineage(self):
        s = Statement()
        s2 = Statement()
        s3 = Statement()
        s3.from_lineage([s, s2])
        assert s.scope[0] is s2
        child = s.scope[0]
        assert child.scope[0] is s3

    def test_build_renderer(self):
        s = Statement()
        renderer = s.build_renderer()
        print type(renderer)
        assert isgenerator(renderer)

    def test_render(self):
        s_base = Statement()
        s = Statement(code='for i in range(10):')
        s2 = Statement(code='print i')
        s3 = Statement(code='print "done"')
        s_base.create_lineage([s,s2])
        s_base.add_child(s3)
        test_code = '\n'.join(s_base) # join with \n to replicate a document output
        train_code = '\nfor i in range(10):\n    print i\nprint "done"'
        assert test_code == train_code

    def test_to_statement(self):
        init = Statement("TESTING")
        from_string = Statement.to_statement("TESTING")
        from_state = Statement.to_statement(init)
        from_int = Statement.to_statement(4)
        assert isinstance(from_string, Statement)
        assert from_state is init
        assert isinstance(from_int, Statement)

    def test_to_statement(self):
        assert Statement("TEST").__str__() == "TEST"

    def test_to_statement_type(self):
        assert isinstance(Statement("TEST"), Statement)

    def test_to_statement_identity(self):
        s = Statement("TEST")
        assert s is Statement.to_statement(s)

    def test_to_statement_name(self):
        assert Statement(Name("TEST")).__str__() == "TEST"

    def test_to_statement_num(self):
        assert Statement(Num(4)).__str__() == "4"

    def test_to_statement_func(self):
        assert Statement(FunctionDef(name="func",
                                     arg_names=['a','b'],
                                     kwarg_pairs={"x":"y"},
                                     varargs="args",
                                     keywords="kwargs")).__str__() == "def func(a, b, x=y, *args, **kwargs):"

    def test_to_statement_decorator(self):
        assert Statement(DecoratorDef(name="func")).__str__() == '@func()'

    def test_to_statement_class(self):
        assert Statement(ClassDef(name="cls")).__str__() == 'class cls():'

    def test_to_statement_attribute(self):
        assert Statement(Attribute(name="thing",
                         caller_list=['a', 'b', 'c'])).__str__() == 'a.b.c.thing'

    def test_to_statement_call(self):
        assert Statement(Call(name="thing",
                    caller_list=['a', Statement('b'), 'c'])).__str__() == 'a.b.c.thing()'


class TestName():

    valid_function_names = ['_func', '_Func', 'func_', 'Func_']

    invalid_sourcerer_function_names = [Statement('1_func'), Name('1_Func'), Str('1func_'), '1Func_']
    valid_sourcerer_function_names = valid_function_names

    invalid_int_function_names = ['1_func', '1_Func', '1func_', '1Func_']
    valid_int_function_names = valid_function_names

    invalid_punc_function_names = ['(_func', '(_Func', '(func_', '(Func_',
                                   '_func(', '_Func(', 'func_(', 'Func_(',
                                   '_(func', '_(Func', 'func(_', 'Func(_']
    valid_punc_function_names = ['_func', '_Func', 'func_', 'Func_',
                                 '_func', '_Func', 'func_', 'Func_',
                                 '_func', '_Func', 'func_', 'Func_']

    invalid_mixed_function_names = ['(1_1func', '1(_1Func', '1(1func_', '1(1Func_',
                                   '1_func(1', '_1Func1(', 'func1_(1', 'Func_1(1',
                                   '1_(1func', '_1(Func1', 'func1(1_', '1Func(_1']
    valid_mixed_function_names = ['_1func', '_1Func', 'func_', 'Func_',
                                   '_func1', '_1Func1', 'func1_1', 'Func_11',
                                   '_1func', '_1Func1', 'func11_', 'Func_1']

    def test_format(self):
        # Make sure we are getting rid of those quotes so we get name and not 'name'
        for valid in self.valid_function_names:
            assert Name(valid).__str__() == valid
            assert Name(valid) != valid

    def test_invalid_sourcerer(self):
        for invalid, valid in zip(self.invalid_sourcerer_function_names, self.valid_sourcerer_function_names):
            assert Name(invalid).__str__() == valid

    def test_invalid_int(self):
        for invalid, valid in zip(self.invalid_int_function_names, self.valid_int_function_names):
            assert Name(invalid).__str__() == valid

    def test_invalid_punc(self):
        for invalid, valid in zip(self.invalid_punc_function_names, self.valid_punc_function_names):
            assert Name(invalid).__str__() == valid

    def test_invalid_mixed(self):
        for invalid, valid in zip(self.invalid_mixed_function_names, self.valid_mixed_function_names):
            assert Name(invalid).__str__() == valid

    def test_dont_validate(self):
        for invalid in self.invalid_mixed_function_names:
            assert Name(invalid, validate=False).__str__() == invalid


class TestStr():

    def test_str_double(self):
        assert Str("hello").__str__() == '"hello"'

    def test_str_statement_double(self):
        assert Str(Statement("hello")).__str__() == '"hello"'

    def test_str_double_str_double(self):
        assert Str(Str("hello")).__str__() == '"hello"'

    def test_str_single_str_double(self):
        assert Str(Str("hello", True)).__str__() == '"hello"'

    def test_str_complex_double(self):
        assert Str("h'el*l\"o").__str__() == '"h\'el*l\\"o"'

    def test_str_single(self):
        assert Str("hello", True).__str__() == "'hello'"

    def test_str_statement_single(self):
        assert Str(Statement("hello"), True).__str__() == "'hello'"

    def test_str_single_str_single(self):
        assert Str(Str("hello", True), True).__str__() == "'hello'"

    def test_str_double_str_single(self):
        assert Str(Str("hello"), True).__str__() == "'hello'"

    def test_str_complex_single(self):
        assert Str("h'el*l\"o", True).__str__() == '\'h\\\'el*l"o\''


class TestNum():

    def test_string_to_num(self):
        assert Num("6").__str__() == "6"

    def test_statement_to_num(self):
        assert Num(Statement("6")).__str__() == "6"

    def test_num_to_num(self):
        assert Num(Num("6")).__str__() == "6"

    def test_int_to_num(self):
        assert Num(6).__str__() == "6"

    def test_signed_to_num(self):
        assert Num(-6).__str__() == "-6"

    def test_float_to_num(self):
        assert Num(6.6).__str__() == "6.6"

    def test_long_to_num(self):
        assert Num(long(6)).__str__() == "6"

    def test_complex_to_num(self):
        assert Num(6j).__str__() == "6j"


# Test Callables
class TestFunctionDef():

    def test_function_name(self):
        assert FunctionDef(name="func").__str__() == 'def func():'

    def test_function_name_statement(self):
        assert FunctionDef(name=Statement("func")).__str__() == 'def func():'

    def test_function_name_name(self):
        assert FunctionDef(name=Name("func")).__str__() == 'def func():'

    def test_function_name_str(self):
        assert FunctionDef(name=Str("func")).__str__() == 'def func():'

    def test_arg_names(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", "a2"]).__str__() == 'def func(a1, a2):'

    def test_arg_names_statement(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", Statement("a2")]).__str__() == 'def func(a1, a2):'

    def test_arg_names_name(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", Name("a2")]).__str__() == 'def func(a1, a2):'

    def test_arg_names_str(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", Str("a2")]).__str__() == 'def func(a1, "a2"):'

    def test_arg_names_call(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", Call(name="a2")]).__str__() == 'def func(a1, a2()):'

    def test_arg_names_caller_list(self):
        assert FunctionDef(name="func",
                           arg_names=["a1", Call(name="a2", caller_list=['a'])]).__str__() == 'def func(a1, a.a2()):'

    def test_kwarg_pairs(self):
        assert FunctionDef(name="func",
                           kwarg_pairs={"a1":Str("a2")}).__str__() == 'def func(a1="a2"):'

    def test_kwarg_pairs_many(self):
        fields = {"chris":1, "jon":2, "kevin":3, "sam":4, "other":5, "thing":6, "ashley":7}
        ouputs = []
        for i in range(100):
            doc = Document()
            func_obj = [FunctionDef(name="func", kwarg_pairs=fields),
                        Return(Statement("[chris, jon, kevin, sam, other, thing, ashley]"))]
            doc.create_lineage(func_obj)
            exec(doc.output())
            assert func() == [1, 2, 3, 4, 5, 6, 7]

    def test_kwarg_pairs_statement(self):
        assert FunctionDef(name="func",
                           kwarg_pairs={"a1":Statement("a2")}).__str__() == 'def func(a1=a2):'

    def test_kwarg_pairs_name(self):
        assert FunctionDef(name="func",
                           kwarg_pairs={"a1":Name("a2")}).__str__() == 'def func(a1=a2):'

    def test_kwarg_pairs_call(self):
        assert FunctionDef(name="func",
                           kwarg_pairs={"a1":Call(name="a2")}).__str__() == 'def func(a1=a2()):'

    def test_kwarg_pairs_call_list(self):
        assert FunctionDef(name="func",
                           kwarg_pairs={"a1":Call(name="a2", caller_list=['a'])}).__str__() == 'def func(a1=a.a2()):'

    def test_star_args(self):
        assert FunctionDef(name="func",
                           varargs="args").__str__() == 'def func(*args):'

    def test_star_args_statement(self):
        assert FunctionDef(name="func",
                           varargs=Statement("args")).__str__() == 'def func(*args):'

    def test_star_args_name(self):
        assert FunctionDef(name="func",
                           varargs=Name("args")).__str__() == 'def func(*args):'

    def test_sskwargs(self):
        assert FunctionDef(name="func",
                           keywords="kwargs").__str__() == 'def func(**kwargs):'

    def test_sskwargs_statement(self):
        assert FunctionDef(name="func",
                           keywords=Statement("kwargs")).__str__() == 'def func(**kwargs):'

    def test_sskwargs_name(self):
        assert FunctionDef(name="func",
                           keywords=Name("kwargs")).__str__() == 'def func(**kwargs):'


class TestDecoratorDef():

    def test_function_name(self):
        assert DecoratorDef(name="func").__str__() == '@func()'

    def test_function_name_statement(self):
        assert DecoratorDef(name=Statement("func")).__str__() == '@func()'

    def test_function_name_name(self):
        assert DecoratorDef(name=Name("func")).__str__() == '@func()'

    def test_function_name_attribute(self):
        assert DecoratorDef(name=Attribute(name="func", caller_list=['a'])).__str__() == '@a.func()'

    def test_arg_names(self):
        assert DecoratorDef(name="func",
                           arg_names=["a1", "a2"]).__str__() == '@func(a1, a2)'

    def test_arg_names_statement(self):
        assert DecoratorDef(name="func",
                           arg_names=[Statement("a1"), "a2"]).__str__() == '@func(a1, a2)'

    def test_arg_names_name(self):
        assert DecoratorDef(name="func",
                           arg_names=[Name("a1"), "a2"]).__str__() == '@func(a1, a2)'

    def test_arg_names_str(self):
        assert DecoratorDef(name="func",
                           arg_names=[Str("a1"), "a2"]).__str__() == '@func("a1", a2)'

    def test_kwarg_pairs(self):
        assert DecoratorDef(name="func",
                           kwarg_pairs={"a1":Str("a2")}).__str__() == '@func(a1="a2")'

    def test_kwarg_pairs_statement(self):
        assert DecoratorDef(name="func",
                           kwarg_pairs={Statement("a1"):Statement("a2")}).__str__() == '@func(a1=a2)'

    def test_kwarg_pairs_name(self):
        assert DecoratorDef(name="func",
                           kwarg_pairs={Name("a1"):Name("a2")}).__str__() == '@func(a1=a2)'

    def test_kwarg_pairs_str(self):
        assert DecoratorDef(name="func",
                           kwarg_pairs={Str("a1"):Str("a2")}).__str__() == '@func("a1"="a2")'

    def test_star_args(self):
        assert DecoratorDef(name="func",
                           varargs="args").__str__() == '@func(*args)'

    def test_star_args_statement(self):
        assert DecoratorDef(name="func",
                           varargs=Statement("args")).__str__() == '@func(*args)'

    def test_star_args_name(self):
        assert DecoratorDef(name="func",
                           varargs=Name("args")).__str__() == '@func(*args)'

    def test_sskwargs(self):
        assert DecoratorDef(name="func",
                           keywords="kwargs").__str__() == '@func(**kwargs)'

    def test_sskwargs_statement(self):
        assert DecoratorDef(name="func",
                           keywords=Statement("kwargs")).__str__() == '@func(**kwargs)'

    def test_sskwargs_name(self):
        assert DecoratorDef(name="func",
                           keywords=Name("kwargs")).__str__() == '@func(**kwargs)'


class TestClassDef():

    def test_function_name(self):
        assert ClassDef(name="cls").__str__() == 'class cls():'

    def test_arg_names(self):
        assert ClassDef(name="cls",
                           arg_names=["a1", "a2"]).__str__() == 'class cls(a1, a2):'

    def test_kwarg_pairs(self):
        assert ClassDef(name="cls",
                           kwarg_pairs={"a1":Str("a2")}).__str__() == 'class cls(a1="a2"):'

    def test_star_args(self):
        assert ClassDef(name="cls",
                           varargs="args").__str__() == 'class cls(*args):'

    def test_sskwargs(self):
        assert ClassDef(name="cls",
                           keywords="kwargs").__str__() == 'class cls(**kwargs):'


class TestAttribute():

    def test_obj_chain(self):
        assert Attribute(name="thing",
                         caller_list=['a', 'b', 'c']).__str__() == 'a.b.c.thing'

    def test_obj_chain_statement(self):
        assert Attribute(name="thing",
                         caller_list=[Statement('a'), Statement('b'), Statement('c')]).__str__() == 'a.b.c.thing'

    def test_obj_chain_name(self):
        assert Attribute(name="thing",
                         caller_list=[Name('a'), Name('b'), Name('c')]).__str__() == 'a.b.c.thing'

    def test_obj_chain_str(self):
        assert Attribute(name="thing",
                         caller_list=[Str('a'), 'b', 'c']).__str__() == '"a".b.c.thing'

    def test_obj_chain_attribute(self):
        attr = Attribute(name="a", caller_list=["a1", "a2"])
        assert Attribute(name="thing",
                         caller_list=[attr, 'b', 'c']).__str__() == 'a1.a2.a.b.c.thing'

    def test_obj_chain_call(self):
        assert Attribute(name="thing",
                         caller_list=['a', Call(name="b"), 'c']).__str__() == 'a.b().c.thing'

    def test_obj_chain_call(self):
        assert Attribute(name=Call(name="thing"),
                         caller_list=['a', Call(name="b"), 'c']).__str__() == 'a.b().c.thing()'


class TestCall():

    def test_call_no_args(self):
        assert Call(name="thing",
                    caller_list=['a', Statement('b'), 'c']).__str__() == 'a.b.c.thing()'

    def test_call_str_args(self):
        assert Call(name="thing",
                    caller_list=['a', 'b', 'c'],
                    arg_names=['x', 'y'],
                    kwarg_pairs={'a1':'1'}).__str__() == 'a.b.c.thing(x, y, a1=1)'

# Test Modules


class TestDocument():

    def test_doc(self):
        d = Document()
        d.add_child(Statement("1 == 1"))
        assert d.output().__str__() == '1 == 1\n'

    def test_yapf(self):
        d = Document()
        d.add_child(Statement("1==1"))
        assert d.output().__str__() == '1 == 1\n'

# Test Simple Statements


class TestReturn():

    def test_return_empty(self):
        assert Return().__str__() == 'return'

    def test_return(self):
        assert Return("test").__str__() == 'return test'

    def test_yield_empty(self):
        assert Return(_type="yield").__str__() == 'yield'

    def test_yield(self):
        assert Return("test", _type="yield").__str__() == 'yield test'

    def test_pass(self):
        assert Return(_type="pass").__str__() == 'pass'

    def test_return_statement(self):
        assert Return(Statement("test")).__str__() == 'return test'

    def test_return_call(self):
        c = Call(name="thing", caller_list=['a', Statement('b'), 'c'], arg_names=['x'])
        assert Return(c).__str__() == 'return a.b.c.thing(x)'


class TestDocString():

    def test_docstring(self):
        assert Docstring("test").__str__() == '"""test\n\n"""'

    def test_docstring_statement(self):
        assert Docstring(Statement("test")).__str__() == '"""test\n\n"""'

    def test_docstring_call(self):
        c = Call(name="thing", caller_list=['a', Statement('b'), 'c'], arg_names=['x'])
        assert Docstring(c).__str__() == '"""a.b.c.thing(x)\n\n"""'

    def test_extended(self):
        d = Docstring("does a thing", extended="more info")
        output = '"""does a thing\n\nmore info\n"""'
        assert d.__str__() == output

    def test_section(self):
        d = Docstring("does a thing", extras={"Args":[
            {"id":"arg1", "param_type":"int", "description":"the first arg"},
            {"id":"arg2", "description":"the second arg"}
        ]})
        output = '"""does a thing\n\nArgs:\narg1 (int): the first arg\narg2: the second arg\n"""'
        assert d.__str__() == output

    def test_extended_and_section(self):
        d = Docstring("does a thing", extended="more info", extras={"Args":[
            {"id":"arg1", "param_type":"int", "description":"the first arg"},
            {"id":"arg2", "description":"the second arg"}
        ]})
        output = '"""does a thing\n\nmore info\n\nArgs:\narg1 (int): the first arg\narg2: the second arg\n"""'
        assert d.__str__() == output

    def test_none_docstring(self):
        d = Docstring(extended="more info", extras={"Args":[
            {"id":"arg1", "param_type":"int", "description":"the first arg"},
            {"id":"arg2", "description":"the second arg"}
        ]})
        output = '"""\n\nmore info\n\nArgs:\narg1 (int): the first arg\narg2: the second arg\n"""'
        assert d.__str__() == output

    def test_none_extended(self):
        d = Docstring("does a thing", extras={"Args":[
            {"id":"arg1", "param_type":"int", "description":"the first arg"},
            {"id":"arg2", "description":"the second arg"}
        ]})
        output = '"""does a thing\n\nArgs:\narg1 (int): the first arg\narg2: the second arg\n"""'
        assert d.__str__() == output

    def test_section_id_none(self):
        d = Docstring("does a thing", extras={"Args":[
            {"param_type":"int", "description":"the first arg"}]})
        output = '"""does a thing\n\nArgs:\n(int): the first arg\n"""'
        assert d.__str__() == output

    def test_section_param_none(self):
        d = Docstring("does a thing", extras={"Args":[
            {"id":"arg1", "description":"the first arg"}]})
        output = '"""does a thing\n\nArgs:\narg1: the first arg\n"""'
        assert d.__str__() == output

    def test_section_description_none(self):
        d = Docstring("does a thing", extras={"Args":[
            {"id":"arg1", "param_type":"int"}]})
        output = '"""does a thing\n\nArgs:\narg1 (int)\n"""'
        assert d.__str__() == output


class TestAssignment():

    def test_assignment(self):
        assert Assignment('x', '1').__str__() == 'x = 1'

    def test_assignment_statement(self):
        assert Assignment(Statement('x'), '1').__str__() == 'x = 1'

    def test_assignment_call(self):
        c = Call(name="thing", caller_list=['a', Statement('b'), 'c'], arg_names=['x'])
        assert Assignment('x', c).__str__() == 'x = a.b.c.thing(x)'