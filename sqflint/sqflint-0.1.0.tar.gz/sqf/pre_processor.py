# def _check_define_param(param, statement=None):
#     exceptions = []
#     if type(param) == Variable:
#         add = str(param)
#     elif isinstance(param, Keyword):
#         exceptions.append(SQFWarning(param.position, 'redefining keyword "%s".' % str(param)))
#         add = str(param)
#     else:
#         add = None
#         exceptions.append(SQFParserError(param.position, 'invalid 1st argument'))
#
#     if add is not None and statement is not None:
#         if type(statement) != Statement or not statement.parenthesis:
#             exceptions.append(SQFParserError(statement.position, 'wrong construction'))
#             add = None
#
#     return exceptions, add
#
#
# # pre-process #defines
# if base_tokens and base_tokens[0] == Keyword('#define'):
#     tokens = statement._tokens
#     spaces_positions = [i for i,t in enumerate(statement._tokens) if t == Space()]
#     if len(spaces_positions) not in [1, 2]:
#         self.exception(SQFParserError(base_tokens[0].position, '#define must contain exactly 1 or 2 arguments'))
#     elif len(spaces_positions) == 1:
#         self.defines[str(base_tokens[1])] = Nothing
#     elif len(spaces_positions) == 2:
#         arg1 = tokens[spaces_positions[0]+1:spaces_positions[1]]
#         arg2 = tokens[spaces_positions[1]+1:]
#         if len(arg1) == 1:
#             arg1 = arg1[0]
#             exceptions, add = _check_define_param(arg1)
#             if exceptions:
#                 self.exceptions += exceptions
#             if add is not None:
#                 self.defines[add] = arg2
#         elif len(arg1) == 2:  # of the form #define a(...) b
#             exceptions, add = _check_define_param(arg1[0], arg1[1])
#             if exceptions:
#                 self.exceptions += exceptions
#             if add is not None:
#                 self.defines[add] = arg2
#         else:
#             self.exception(SQFParserError(tokens[0].position, '#define 1st argument is invalid'))
#
#     return Nothing
#
#
# def is_parenthesis_statement(statement):
#     if isinstance(statement, Statement):
#         if statement.parenthesis == '()':
#             return True
#         else:
#             assert(len(statement.base_tokens) > 0)
#             return is_parenthesis_statement(statement.base_tokens[0])
#     return False
