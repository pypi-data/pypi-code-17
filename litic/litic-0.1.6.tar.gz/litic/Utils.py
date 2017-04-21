import re, csv, sys

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        if sys.version_info >= (3, 0):
            yield [cell for cell in row]
        else:
            yield [unicode(cell, 'utf-8') for cell in row]

def extract_header_format(name):
    type = None
    matches = re.match(r"(.+)(\{[^\{\}]+\})$", name)
    if matches is not None:
        tmpstr2 = matches.group(1)
        tmpstr2 = tmpstr2.strip()
        # tmpstr = matches.group(2)
        # tmpstr = tmpstr.strip()
        # tmpstr = tmpstr[1:len(tmpstr) - 2]
        # tmpstr = tmpstr.strip()
        name = tmpstr2
        # type = tmpstr
    matches = re.match(r"(.+)(\[[^\[\]]+\])$", name)
    if matches is not None:
        tmpstr2 = matches.group(1)
        tmpstr2 = tmpstr2.strip()
        name = tmpstr2
    return name, type
