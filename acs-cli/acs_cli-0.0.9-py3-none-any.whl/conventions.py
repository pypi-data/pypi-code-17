import re


def camel_to_dashed(camel):
    return re.sub('([a-z])([A-Z])', '\g<1>-\g<2>', camel).lower()
