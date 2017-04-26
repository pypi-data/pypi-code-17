import datetime
import re
import threading

from wxpy.utils import start_new_thread


class Tasks(list):
    def __init__(self):
        super(Tasks, self).__init__()
        self._pending = None

    def incoming(self, n=10):
        """
        用于查看即将执行的 n 个任务

        :param n: 即将执行的任务个数 n
        :return: 即将执行的 n 个任务
        """

        scheduled = list()
        rounds = {task: 0 for task in self}

        for _ in range(n):
            choices = tuple(filter(
                lambda x: x[0],
                ((task.next_datetime(rounds[task] + 1), task) for task in self)
            ))
            if not choices:
                break
            _datetime, task = min(choices)
            scheduled.append((_datetime, task))
            rounds[task] += 1

        return scheduled

    def append(self, task):
        super(Tasks, self).append(task)
        self._update_pending()

    def _update_pending(self):
        if isinstance(self._pending, threading.Timer):
            self._pending.cancel()
        


def _valid_n(n):
    """
    验证 n 参数是否合法
    """

    if not isinstance(n, int):
        raise TypeError('expected int, got {}'.format(type(n)))
    elif n < 1:
        raise ValueError('expected n >= 1')


class BaseTask(object):
    def __init__(self, func, args=(), kwargs=None):
        self.func = func or tuple()
        self.args = args or dict()
        self.kwargs = kwargs
        self.thread = None

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            self.func.__name__,
        )

    def run(self):

        self.thread = start_new_thread(
            target=self.func, args=self.args, kwargs=self.kwargs)

    @property
    def is_alive(self):
        if isinstance(self.thread, threading.Thread):
            return self.thread.is_alive()

    def join(self):
        if self.is_alive:
            self.thread.join()

    def next_datetime(self, n=1):
        """
        | 返回接下来的第 n 次执行的时间点 (datetime.datetime)
        | 由子类实现
        
        :param n: 接下来的第 n 次执行的次数
        """

        raise NotImplementedError


class TimerTask(BaseTask):
    def __init__(
            self, func, seconds=0, minutes=0, hours=0,
            times=1, args=(), kwargs=None
    ):
        """
        添加定时任务 (例如: 3 分 30 秒 后执行)

        :param func: 待执行的函数
        :param seconds: 秒数
        :param minutes: 分钟数
        :param hours: 小时数
        :param times: 执行的次数，为负数时表示一直重复
        :param args: 位置参数
        :param kwargs: 命名参数
        """

        super(TimerTask, self).__init__(func=func, args=args, kwargs=kwargs)

        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.times = times

    def next_datetime(self, n=1):
        _valid_n(n)
        if n <= self.times or self.times < 0:
            return datetime.datetime.now() + datetime.timedelta(
                seconds=self.seconds, minutes=self.minutes, hours=self.hours
            ) * n


class DatetimeTask(BaseTask):
    RE_Y = r'^(?P<year>\d{4})?\b'

    RE_MD = \
        r'(?:^|-)(?:(?P<month>\d{1,2})' \
        r'-(?P<day>\d{1,2}))?(?:$|\b)'

    RE_HMS = \
        r'(?:\b| +)(?P<hour>\d{1,2})?' \
        r'(?::(?P<minute>\d{1,2}))?' \
        r'(?::(?P<second>\d{1,2}))?(?:$)'

    RP_DATETIME = re.compile(RE_Y + RE_MD + RE_HMS)

    def __init__(self, func, datetime_, args=(), kwargs=None):
        """
        添加指定日期时间的任务 (例如: 2017-4-1 9:30:00 执行)
        :param func: 待执行的函数
        :param datetime_:
            指定的日期时间，支持以下类型的值:
                * 字符串: 例如 '2017-4-1 9:30:00'
                    * 格式为 '年份-月份-日期 时:分:秒'
                    * 除年份必须为 4 位数外，其他均可为 1 或 2 位数字
                    * 日期为必填部分，年份为可选部分，时分秒可省略结尾部分
                        * 年份被省略时，匹配下一次最近的日期
                        * 时分秒的尾部被省略时，省略部分作为 0
                * datetime 时间戳: 例如 datetime.datetime(2017, 4, 1, 9, 30, 0)
        :param args: 位置参数
        :param kwargs: 命名参数
        """

        super(DatetimeTask, self).__init__(func=func, args=args, kwargs=kwargs)

        if isinstance(datetime_, str):
            self.datetime = self._get_datetime_from_text(datetime_)
        elif isinstance(datetime_, datetime.datetime):
            self.datetime = datetime_
        else:
            raise TypeError('expected str or datetime.datetime, got {}'.format(type(datetime_)))

        if self.datetime <= datetime.datetime.now():
            raise ValueError(
                'should be a future datetime, got {:%Y-%m-%d %H:%M}'.format(self.datetime))

    def _get_datetime_from_text(self, text):

        exception_msg = 'invalid datetime string: {}'.format(text)

        try:
            _datetime = self.RP_DATETIME.search(text).groupdict()
        except AttributeError:
            raise ValueError(exception_msg)

        for k in _datetime:
            _datetime[k] = int(_datetime[k] or 0)

        if _datetime['year'] and not _datetime['day']:
            raise ValueError(exception_msg)

        for attr in 'day', 'month', 'year':
            _datetime[attr] = _datetime[attr] or getattr(datetime.datetime.now(), attr)
        return datetime.datetime(**_datetime)

    def next_datetime(self, n=1):
        if n == 1:
            return self.datetime


if __name__ == '__main__':
    def test(*args, **kwargs):
        print(args, kwargs)


    print(DatetimeTask(test, datetime.datetime.now() + datetime.timedelta(seconds=1)).datetime)

    # tasks = Tasks()
    # tasks.append(TimerTask(test, args=(3, '4'), kwargs=dict(a=1, b=2, c=3), hours=1, times=-1))
    # pprint(tasks.incoming(5))
