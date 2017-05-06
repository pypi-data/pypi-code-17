import re
from wtforms import ValidationError


def check_length(data, min=0, max=None, nullable=True):
    if data:
        l = len(data)
        if min:
            if l < min:
                raise ValidationError('length<{0}'.format(min))
        if max:
            if l > max:
                raise ValidationError('length>{0}'.format(max))
    else:
        if (min != 0) or (not nullable):
            raise ValidationError('cannot-empty')

def check_uuid(data, nullable=True):
    if data:
        regex = re.compile(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$')
        match = regex.match(data or '')
        if not match:
            raise ValidationError('invalid-id')
    else:
        if not nullable:
            raise ValidationError('data-required')

def check_number(n, min=None, max=None):
    if min:
        if n < min:
            raise ValidationError('<{0}'.format(min))
    if max:
        if n > max:
            raise ValidationError('>{0}'.format(max))

def check_bool_string(data, nullable=True):
    if data:
        if data not in ("true", "false"):
            raise ValidationError('true-or-false')
    else:
        if not nullable:
            raise ValidationError('true-or-false')

def true_or_false_or_empty(form, field):
    if field.data:
        # TODO: Important! 统一为 bool
        if field.data not in (True, False, "true", "false"):
            raise ValidationError('Field must be "true", or "false", or empty')
