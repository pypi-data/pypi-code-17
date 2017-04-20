from sourcerer import FunctionDef, Return


base_syntax = {"functions": {'type': FunctionDef,
                             'key': 'name',
                             'value_map': {'args': 'arg_names',
                                           'kwargs': 'kwarg_pairs',
                                           'varargs': 'varargs',
                                           'keywords': 'keywords'},
                              'children':{'ret':'return'}},
  "return": {'type': Return,
             'key': None,
             'value_map': {'value':'val'}}
 }

yaml_syntax = base_syntax
