import re

def strspn(source, allowed):
    newchrs = []
    for c in source:
        if c in allowed:
            newchrs.append(c)
    return u''.join(newchrs)

def firstmatch(source, regexes):
    for regex in regexes:
        match = re.match(regex, source)
        if match is not None:
            return match.groups()[0]
    return None

def check_belgian_cell_phone_number(number):
    cleaned_number = strspn(number, u'+0123456789')
    cleaned_number = firstmatch(cleaned_number, [r'^04(\d{8})$', r'^324(\d{8})$', r'^\+324(\d{8})$', r'^\+3204(\d{8})$', r'^4(\d{8})$', r'^00324(\d{8})$'])

    if cleaned_number is None:
        return None

    return u'+324%s' % cleaned_number

def check_cell_phone_number(number):
    if number[:1] != '+':
        belgian = check_belgian_cell_phone_number(number)
        if belgian is not None:
            return belgian

    cleaned_number = strspn(number, u'+0123456789')
    cleaned_number = firstmatch(cleaned_number, [r'^(\+\d{11})$', r'^(\+\d+)$'])

    if cleaned_number is None:
        return None

    return u'%s' % cleaned_number
