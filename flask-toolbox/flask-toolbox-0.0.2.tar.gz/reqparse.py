"""
请求解析
"""
from flask import request

from . import errors


class RequestParser(object):
    """
    请求解析器
    """

    def __init__(self):
        self.arguments = {}

    def add_argument(self, name, **kwargs):
        """
        添加需要解析的参数
        :param name: 参数名
        :param target: 参数目标字段
        :param type: 类型,需要是一个function类型的值
        :param required: 是否是必须的
        :param nullable: 是否可为空
        :param location: 参数的位置,支持str 和 list 类型的参数,其中值可以为 values headers args from cookies files
        :param default: 默认值
        :param help: 出现错误时提示内容
        :return: 
        """
        location = kwargs.get('location', 'values')
        if isinstance(location, list):
            values = [getattr(request, loc) for loc in location]
        else:
            values = [(getattr(request, location)), ]
        self.arguments[name] = {
            'target': kwargs.get('target', name),
            'type': kwargs.get('type', str),
            'required': kwargs.get('required', False),
            'nullable': kwargs.get('nullable', True),
            'default': kwargs.get('default', None),
            'values': values,
            'help': kwargs.get('help', 'error'),
        }

    def parse_args(self):
        """
        解析参数
        :return: 
        """
        args = {}
        for name, kwargs in self.arguments.items():
            target = kwargs.get('target')
            values = kwargs.get('values')
            values.reverse()
            arg = None
            is_arg_exist = False  # 标记是否存在参数
            for value in values:
                is_arg_exist = target in value
                if is_arg_exist:
                    arg = value.get(target)
                    break
            if kwargs.get('required') and not is_arg_exist:
                raise errors.InvalidUsage(message=kwargs.get('help'))
            if arg is None:
                # 参数为空
                arg = kwargs.get('default')
            else:
                try:
                    arg = kwargs.get('type')(arg)
                except ValueError:
                    raise errors.InvalidUsage(message=kwargs.get('help'))
            if not kwargs.get('nullable') and not arg:
                # 参数不能为空且参数为空
                raise errors.InvalidUsage(message=kwargs.get('help'))
            args[name] = arg
        return args
