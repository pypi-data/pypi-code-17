# -*- coding:utf-8 -*-
from abc import abstractmethod
from Queue import Queue
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class DataSource(object):
    __doc__ = '''
        Source base class.
        It contains the material of a spider, such as urls, parameters.
        
        Warning: DataSource class and its derived classes must be iterable, otherwise the spider could not acquire 
        any information. 
        
        If there is no more data in data source, the program will pause waiting for the new data append in.
    '''

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __iter__(self):
        pass


class CocoQueue(DataSource):
    __doc__ = '''
        Package class of Queue.
        This class provides simple operations onto queue.
        User should use a Queue object to initialize this class.
    '''

    def __init__(self, q=Queue(),data=list(), **kwargs):
        super(CocoQueue, self).__init__(**kwargs)
        self.queue = q
        for i in data:
            self.append(i)

    def __iter__(self):
        while True:
            if self.queue.empty():
                logging.debug("Queue has no more data, waiting...")
            yield self.pop()

    def append(self, obj):
        self.queue.put(obj)

    def pop(self):
        return self.queue.get()


class CocoRedis(DataSource):
    __doc__ = '''
        Package class of redis.
        This class provides simple operations onto redis.
        This class just offer READ-ONLY interface.
        However, user should construct a connection previously, and provides a redis key
    '''

    def __init__(self, client, key, **kwargs):
        super(CocoRedis, self).__init__(**kwargs)
        self.client = client
        self.key = key

    def __iter__(self):
        logged = False
        while True:
            url = self.client.spop(self.key)
            if url:
                logged = False
                yield url
            else:
                if not logged:
                    logging.warning("Redis has no more data in %s, waiting..." % self.key)
                    logged = True
                continue
