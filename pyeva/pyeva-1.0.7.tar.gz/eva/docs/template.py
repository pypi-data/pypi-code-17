import os

import mako.runtime
from mako.template import Template
from mako.lookup import TemplateLookup

# 相关路径
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# 初始化 mako
mako.runtime.UNDEFINED = '' # 未定义的变量不会出错

mylookup = TemplateLookup(directories=[PROJECT_ROOT], input_encoding="utf-8")

def find_template(name):
    return mylookup.get_template(name)
