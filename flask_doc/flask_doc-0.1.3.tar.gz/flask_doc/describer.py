# coding=utf8
from functools import wraps

import logging
from flask import request
from utils import func_sign

api_forms ={}
api_args = {}

form_data = {}
args_data = {}


def _is_float(s):
    return sum([n.isdigit() for n in s.strip().split('.')]) == 2

def gathering_form(ins):
    """
    生成一个类的实例, 然后将form或者args的内容, 付给这个类实例的属性
    :param ins: 
    :type ins: 
    :return: 
    :rtype: 
    """
    for k, v in form_data.iteritems():
        if hasattr(ins, k):
            setattr(ins, k, v)
    return ins


def gathering_args(ins):
    """
    生成一个类的实例, 然后将form或者args的内容, 付给这个类实例的属性
    :param ins: 
    :type ins: 
    :return: 
    :rtype: 
    """
    for k, v in args_data.iteritems():
        if hasattr(ins, k):
            setattr(ins, k, v)
    return ins


class FieldDescribe(object):
    filed_name = ''
    required = True
    data_type = None
    help = ''

    def __repr__(self):
        return u"%s-%s-%s-%s" % (self.filed_name, self.required, self.data_type, self.help)

    def get_arr(self):
        return [self.filed_name, str(self.required), str(self.data_type).split("'")[1], self.help]

    def validate(self, dict):
        value = dict.get(self.filed_name)
        if self.required:
            assert value, u"%s不能为空" % self.filed_name
        if self.data_type == type(0.0):
            if not value.isdigit():
                assert _is_float(value), u"%s应该为浮点型,当前值%s" % (self.filed_name, value)
            return float(value)
        if self.data_type == type(0):
            assert value.isdigit(), u"%s必须为数字,当前值%s" % (self.filed_name, value)
            return int(value)
        return value
        

def regist_fields (f, field_name, required, data_type, help, is_form=False):
    desc = FieldDescribe()
    desc.filed_name = field_name
    desc.required = required
    desc.data_type = data_type
    desc.help = help
    f_name = func_sign(f)
    if is_form:
        if f_name in api_forms:
            api_forms[f_name].append(desc)
        else:
            api_forms[f_name] = [desc]
    else:
        if f_name in api_args:
            api_args[f_name].append(desc)
        else:
            api_args[f_name] = [desc]

    return desc

def forms(field_name, required, data_type, help=''):
    def decorator(f):
        desc = regist_fields(f, field_name, required, data_type, help, is_form=True)
        @wraps(f)
        def d_function(*args, **kwargs):
            value = desc.validate(request.form)
            form_data[field_name] = value
            ret_value = f(*args, **kwargs)
            form_data.clear()
            return ret_value
        return d_function
    return decorator


def args(field_name, required, data_type, help=''):
    def decorator(f):
        desc = regist_fields(f, field_name, required, data_type, help)
        @wraps(f)
        def d_function (*args, **kwargs):
            value = desc.validate(request.args)
            args_data[field_name] = value
            ret_value = f(*args, **kwargs)
            args_data.clear()
            return ret_value
        return d_function
    return decorator