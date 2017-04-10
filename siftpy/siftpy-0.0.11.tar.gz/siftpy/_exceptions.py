from __future__ import absolute_import, division, print_function, unicode_literals

class OperatorException(Exception): pass
class OperationException(Exception): pass
class ContextPropertyException(Exception): pass
class PropertyDoesNotExistException(Exception): pass
class InvalidChoiceException(Exception): pass
class ValidationException(Exception): pass
class FlowException(Exception): pass