import datetime
import random
import re

from django.contrib.auth import get_user_model
from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from django.utils.safestring import mark_safe


def is_years_ago(verify_date, years, start_date=None):
    if start_date is None:
        if isinstance(verify_date, datetime.datetime):
            start_date = datetime.datetime.now()
        else:
            start_date = datetime.date.today()

    try:
        start_date = start_date.replace(year=start_date.year - years)
    except ValueError:
        if start_date.month == 2 and start_date.day == 29:
            start_date = start_date.replace(month=2, day=28,
                                            year=start_date.year - years)

    return (verify_date - start_date).days > 0


def unique_username(probe):
    User = get_user_model()
    exists = lambda p: User.objects.filter(username__iexact=p).count() > 0

    if exists(probe):
        counter = 1
        newprobe = '%s%i' % (probe, counter)
        while exists(newprobe):
            counter += 1
            newprobe = '%s%i' % (probe, counter)
        probe = newprobe

    return probe


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


def check_cell_phone_number(number):
    cleaned_number = strspn(number, u'+0123456789')
    cleaned_number = firstmatch(cleaned_number, [r'^04(\d{8})$', r'^324(\d{8})$', r'^\+324(\d{8})$', r'^\+3204(\d{8})$', r'^4(\d{8})$', r'^00324(\d{8})$'])

    if cleaned_number is None:
        return None

    return u'+324%s' % cleaned_number


class Dummy(object):
    def __unicode__(self):
        return self.str

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class HtmlHelpText(Promise):
    def __init__(self, str, **kwargs):
        self.str = str
        self.kwargs = kwargs

    def __unicode__(self):
        return mark_safe(self.str % self.kwargs)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __eq__(self, other):
        return force_unicode(self) == force_unicode(other)


def generate_code(min_length=7, max_length=12, alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    length = len(alphabet)
    if min_length == max_length:
        code_length = min_length
    else:
        code_length = random.randrange(min_length, max_length)
    res = map(lambda x: alphabet[random.randrange(length)], range(code_length))
    return ''.join(res)
