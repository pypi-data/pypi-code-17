'''
The core idea of the reader client is to return
iterable of full object graphs of some entities
as a python dict.
'''
import ftplib
import os
import socket
from ftplib import FTP
from shutil import rmtree
from time import time, sleep

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from data.clients.utils.files_utils import assure_new
from stats.models import Statistics
from .importer import SkipItem
from .networking import SessionPool, ExtSession


def batch_qs(qs, batch_size=1000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:
        # Make sure to order your queryset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])


class BaseReader(object):
    '''
    Usage:

    >>> reader = BaseReader(foo=baz)
    >>> for data in reader:
    >>>     put_to_db(data)
    '''

    def __init__(self, *args, **kwargs):
        '''
        Override this method to provide initial state for reader.
        As an example we can use date_from:

        def __init__(self, date_from=None, *args, **kwargs):
            super(ReaderClassName, )
        '''
        self.kwargs = kwargs
        self.importer = kwargs['importer']
        # self.mongo = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        # self.db = self.mongo[self.importer.source_name]

    def __iter__(self):
        self.before_all()

        for unit in self.data_stream():
            try:
                self.before_unit(unit)
                unit = self.process_unit(unit)
                yield unit
            except SkipItem:
                self.importer.logger.error('skipping item %s at reader', unit)
                continue

            self.after_unit(unit)
        self.after_all()

    def data_stream(self):
        '''
        Here we return some data about entities we store in our db.
        In case it's partial data - you have to provide at least data
        to match with existing documents.
        Redefine this method in case you want to change the behavior of
        reader drastically.
        '''
        raise NotImplementedError

    def process_unit(self, unit):
        '''
        Override this method to perform some postprocessing of initial data.
        Possible options are (not limited to):

        1. Add source name to map be able to get document to update
           (search via source + internal source id (we name it provider_id)).
        2. Convert xml to python dict (we store data as json).
        3. use ujson to deserialize json string from server response.
        4. split a list json response to the list of items and yield them
           one-by-one.

        As a defaut, we return not changed unit.
        '''
        return unit

    def before_all(self):
        '''
        You should override this method to perform some actions before
        import action have started.
        E.g., you can set a starting time here.
        or, you can get a list of all units from source X.
        '''
        self.counter = 0
        self.total_time = 0.0

    def after_all(self):
        '''
        A place to observe state after import have passed.
        '''
        self.importer.logger.info('Total time: %s' % self.total_time)
        self.importer.logger.info('Total actions: %s' % self.counter)

    def before_unit(self, unit):
        self.counter += 1
        self.unit_start = time()

    def after_unit(self, unit):
        self.total_time += time() - self.unit_start


class ApiReader(BaseReader):
    is_paginated = False
    api_keys = ()
    session_class = ExtSession

    def data_stream(self):
        for url in self.get_urls():
            resp = self.grab_data(url)
            if not resp:
                self.importer.logger.error('bad data on url %s' % url)
                continue
            resp_json = resp.json()
            if self.is_paginated:
                for url in self.get_unit_urls(resp_json):
                    data = self.grab_data(url)
                    if not data:
                        self.importer.logger.error('bad data on url %s' % url)
                        continue
                    yield data.json()
            else:
                yield resp_json

    def __init__(self, *args, **kwargs):
        super(ApiReader, self).__init__(*args, **kwargs)
        self.session_pool = SessionPool(
            api_keys=self.api_keys, session_class=self.session_class,
            importer=self.importer
        )

    def get_urls(self):
        raise NotImplementedError(
            'Urls generator got to be defined for every source.'
        )

    def get_unit_urls(self, data):
        raise NotImplementedError(
            'Unit urls generator got to be defined for every paginated source.'
        )

    def grab_data(self, url):
        data = self.session_pool.get(url)
        return data


class BaseFileReader(BaseReader):
    '''
    More basic/broad variant of file-based reader.
    '''
    def __init__(self, *args, **kwargs):
        super(BaseFileReader, self).__init__(*args, **kwargs)
        self.dirname = os.path.join(
            settings.MEDIA_ROOT, self.kwargs['source_name']
        )
        if self.importer.settings.get('clear_folder', False):
            rmtree(self.dirname)
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def data_stream(self):
        for file_url in self.get_urls():
            file_path = self.grab_file(file_url)
            for info_unit in self.get_data_from_file(file_path):
                yield self.process_unit(info_unit)

    def process_unit(self, unit):
        return unit


class FileReader(BaseFileReader):
    '''
    You can subclass me to grab data dumps.
    '''
    def data_stream(self):
        item_id = self.importer.settings.get('item_id')
        if item_id:
            processed_files = self.process_file(item_id)
            counter = 0
            for processed_file in processed_files:
                for item in self.get_filereader(processed_file):
                    counter += 1
                    if not counter % 1000:
                        print(counter)
                    yield item

        for url in self.get_urls():
            with Statistics.stat_dispatch(self.importer, url) as file_stat:
                if file_stat:
                    internal_file = self.grab_file(url=url)
                    processed_files = self.process_file(internal_file)
                    counter = 0
                    for processed_file in processed_files:
                        for item in self.get_filereader(processed_file):
                            counter += 1
                            if not counter % 1000:
                                print(counter)
                            yield item

    def get_urls(self):
        '''
        Returns an iterable of file names to grab.
        '''
        raise NotImplementedError

    def grab_file(self, filename):
        '''
        Returns an absolute path to the grabbed file.
        '''
        raise NotImplementedError

    def process_file(self, path_to_file):
        '''
        You should perform operations on files (like unarchive) here.
        Returns an iterable of paths to files
        '''
        return [path_to_file]

    def get_filereader(self, opened_file):
        '''
        You can use this method to select from:
        xml (etree.iterparse(open(xml_path), tag=self.item_node_name))
        csv (csv.reader(csvfile, delimiter=' ', quotechar='|'))
        or just a simple line-by-line reading (default).

        Returns an iterable.
        '''
        return opened_file.readlines()


class UrlsFromFtp(object):
    ftp_server = None
    ftp_user = 'anonymous'
    ftp_password = ''
    common_dir = '/'

    def __init__(self, *args, **kwargs):
        super(UrlsFromFtp, self).__init__(args, **kwargs)
        if not self.ftp_server:
            raise ImproperlyConfigured('ftp_server not set')

        self.login()

    def login(self):
        self.ftp = FTP(self.ftp_server)
        self.ftp.set_pasv(True)
        self.ftp.login(user=self.ftp_user, passwd=self.ftp_password)

    def ftp_retr(self, filename, buffer):
        try:
            self.importer.logger.info('Downloading ftp://%s/%s' % (self.ftp_server, filename))
            self.ftp.retrbinary('RETR %s' % filename, buffer.write)
        except (ftplib.error_temp, socket.error) as e:
            self.login()
            self.importer.logger.info('error occured [%s], retrying in 10 seconds' % e)
            sleep(10)
            return self.ftp_retr(filename, buffer)
        return buffer

    def download_to_tmp(self, url, dest):
        with open(dest, 'wb') as tmp:
            self.ftp_retr(url, tmp)
            return tmp

    def grab_file(self, url):
        filename = url.split('/')[-1]
        outfile = assure_new(self.dirname, filename)
        self.download_to_tmp(url, outfile)
        self.importer.logger.info('grabbed %s to %s', url, outfile)

        return outfile

    def ftp_ls(self, path):
        return self.ftp.nlst(path)

    def get_urls(self):
        for each in self.ftp_ls(self.common_dir):
            yield each