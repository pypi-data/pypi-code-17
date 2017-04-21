import icu
import datetime
import re


class Calendar:
    """
    Calendar Wrapper based on http://userguide.icu-project.org/datetime/calendar
    """
    _calendar = None
    _locale = None
    _strftime_converts = {
        '%%': '%',
        '%a': 'eee',
        '%A': 'eeee',
        '%w': 'e',
        '%d': 'dd',
        '%-d': 'd',
        '%b': 'MMM',
        '%B': 'MMMM',
        '%m': 'MM',
        '%-m': 'M',
        '%y': 'yy',
        '%Y': 'yyyy',
        '%H': 'HH',
        '%-H': 'H',
        '%I': 'hh',
        '%-I': 'h',
        '%p': 'a',
        '%M': 'mm',
        '%-M': 'm',
        '%S': 'ss',
        '%-S': 's',
        '%f': 'A',
        # '%z': '',
        '%Z': 'zz',
        '%j': 'D'.zfill(3),
        '%-j': 'D',
        # '%U': 'w',
        # '%W': 'w',
        '%c': 'eee MMM dd HH:mm:ss yyyy',
        '%x': 'MM/dd/yy',
        '%X': 'HH:mm:ss',
    }

    def __init__(self, locale: str='en_US', calendar: str=None):
        if calendar is not None:
            locale = '%s@calendar=%s' % (locale, calendar)
        # noinspection PyUnresolvedReferences
        self._locale = icu.Locale.createFromName(locale)
        # noinspection PyUnresolvedReferences
        self._calendar = icu.Calendar.createInstance(self._locale)

        self._strftime_compiled = re.compile("(%s)" % "|".join(map(re.escape, self._strftime_converts.keys())))

    def set_timestamp(self, timestamp):
        """
        Set Timestamp
        :param timestamp: 
        :return: 
        """
        self._calendar.setTime(timestamp)
        return self

    def set_date(self, year, month, day, hour=0, minute=0, second=0):
        """
        Set date and time to current calnedar
        :param year: 
        :param month: 
        :param day: 
        :param hour: 
        :param minute: 
        :param second: 
        :return: 
        """
        month = month-1 if month > 0 else month
        self._calendar.set(year, month, day, hour, minute, second)
        return self

    def get_timestamp(self):
        """
        Get Unix Timestamp of current calendar
        :return: 
        """
        return self._calendar.getTime()

    def get_datetime(self) -> datetime:
        """
        Get Calendar in python datetime
        :return: datetime
        """
        return datetime.datetime.fromtimestamp(self.get_timestamp())

    def get_date(self) -> list:
        """
        Get Calendar date
        :return: 
        """
        result = self.format('yyyy.M.d').split('.')
        return [int(result[0]), int(result[1]), int(result[2])]

    def format(self, pattern: str) -> str:
        """
        Format calendar by ICU pattern http://userguide.icu-project.org/formatparse/datetime
        :param pattern: 
        :return: 
        """
        # noinspection PyUnresolvedReferences
        icu_formatter = icu.SimpleDateFormat(pattern, self._locale)
        return icu_formatter.format(self._calendar)

    def strftime(self, fmt: str) -> str:
        """
        Format calendar as strftime pattern
        References: 
            - ICU: http://userguide.icu-project.org/formatparse/datetime
            - Python Datetime: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    
        :param fmt: str 
        :return: str
        """
        pattern = self._strftime_compiled.sub(lambda m: "'%s'" % self._strftime_converts[m.group().strip()], fmt)
        return self.format(pattern="'%s'" % pattern).strip("'")
