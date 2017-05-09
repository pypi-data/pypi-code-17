# coding=utf-8
from yapf.yapflib.yapf_api import FormatFile

width = 79
style = '{based_on_style: Google, split_before_named_assigns: True, column_limit: ' + str(
    width) + ', SPLIT_ARGUMENTS_WHEN_COMMA_TERMINATED:False}'

fn_in = ['flopymetascript.py', 'model.py', 'parameter.py', 'metafunctions.py',
         '../setup.py', 'version.py', '__init__.py', '__main__.py']

for fn_in_item in fn_in:
    s = FormatFile(fn_in_item, style_config=style)

    with open(fn_in_item, 'w') as f:
        f.write(s[0])
