# -*- coding: utf-8 -*-
import logging
import io
import gzip
import bz2
import time
from gensim.models.doc2vec import TaggedDocument
from pynlple.data.source import Source
from threading import Thread


class IteratorSource(object):

    def __iter__(self):
        pass


class ThreadedStackingSource(IteratorSource):

    def __init__(self, loading_iterator_source, preload=1, num_threads=1):
        self.__items = loading_iterator_source
        self.__queue_size = preload
        self.__queue = list()

    def __iter__(self):
        self.__items_iterator = iter(self.__items)
        self.__load_next()
        self.__curr_item_iterator = self.__next_item_iterator
        self.__next_item_iterator = None
        self.__loader_thread = Thread(target=self.__load_next, args=(self))
        self.__loader_thread.start()
        return self

    def __next__(self):
        if self.__curr_item_iterator:
            try:
                return next(self.__curr_item_iterator)
            except StopIteration:
                self.__curr_item_iterator = None
                return self.__next__()
        else:
            while self.__loader_thread.isAlive():
                time.sleep(0.2)
            if self.__next_item_iterator:
                self.__curr_item_iterator = self.__next_item_iterator
                self.__next_item_iterator = None
                self.__loader_thread = Thread(target=self.__load_next, args=(self))
                self.__loader_thread.start()
                return self.__next__()
            else:
                raise StopIteration()

    def __load_next(self):
        try:
            self.__next_item_iterator = iter(next(self.__items_iterator))
        except StopIteration:
            self.__next_item_iterator = None


class StackingSource(IteratorSource):

    logger = logging.getLogger(__name__)

    def __init__(self, list_sources, log=False):
        self.sources = list_sources
        self.log = log

    def __iter__(self):
        if self.log:
            self.logger.info('[%s] Corpus iterator %s started yielding elements.', str(self.__class__.__name__), repr(self))
        for i_, source in enumerate(self.sources):
            if self.log:
                self.logger.info('[%s] Corpus iterator started yielding elements from source (%d/%d): %s.',
                             str(self.__class__.__name__), i_, len(self.sources), repr(source))
            for item in source:
                yield item


class JsonFieldSource(IteratorSource):

    def __init__(self, json_source, key):
        self.json = json_source
        self.key = key

    def __iter__(self):
        for json_entry in self.json:
            yield json_entry[self.key]


class FilteringSource(IteratorSource):

    def __init__(self, source, condition):
        self.source = source
        self.condition = condition

    def __iter__(self):
        for entry in self.source:
            if self.condition(entry):
                yield entry


class MappingSource(IteratorSource):

    def __init__(self, source, function):
        self.source = source
        self.function = function

    def __iter__(self):
        for entry in self.source:
            yield self.function(entry)


class SplittingSource(IteratorSource):

    def __init__(self, source, splitting_function):
        self.source = source
        self.function = splitting_function

    def __iter__(self):
        for entry in self.source:
            for item in self.function(entry):
                yield item


class DFTaggedDocumentSource(IteratorSource):

    def __init__(self, dataframe_source, text_column, tag_columns=None):
        self.source = dataframe_source
        self.text_column = text_column
        self.tag_columns = tag_columns

    def __iter__(self):
        for row in self.source.get_dataframe().itertuples():
            text = getattr(row, self.text_column)
            tokens = text.split()
            if self.tag_columns:
                yield TaggedDocument(tokens, [getattr(row, tag_column) for tag_column in self.tag_columns])
            else:
                yield tokens


class FileLineSource(IteratorSource):

    def __init__(self, text_file_path, encoding='utf-8'):
        self.source_file = text_file_path
        self.encoding = encoding

    def __iter__(self):
        with io.open(self.source_file, mode='rt', encoding=self.encoding) as in_file:
            for line in in_file:
                line = line.strip()
                if len(line) <= 0:
                    continue
                yield line


class OpensubtitlesSentenceSource(IteratorSource):

    DEFAULT_SENTENCE_TAG = '<s>'

    def __init__(self, line_source, sentence_tag=None):
        self.source = line_source
        if sentence_tag:
            self.sentence_tag = sentence_tag
        else:
            self.sentence_tag = OpensubtitlesSentenceSource.DEFAULT_SENTENCE_TAG

    def __iter__(self):
        for line in self.source:
            for sentence in line.split(self.sentence_tag):
                yield sentence.strip()


class BZipDocumentSource(IteratorSource):

    def __init__(self, bzip_filepath, text_preprocessor=None):
        self.source_filepath = bzip_filepath
        self.text_preprocessor = text_preprocessor
        super().__init__()

    def __iter__(self):
        with bz2.BZ2File(self.source_filepath, 'rtU') as in_bz:
            for line in in_bz:
                text = line
                if self.text_preprocessor:
                    text = self.text_preprocessor.preprocess(text)
                tokens = text.split()
                yield tokens


class GZipDocumentSource(IteratorSource):

    def __init__(self, gzip_filepath, text_preprocessor=None):
        self.source_filepath = gzip_filepath
        self.text_preprocessor = text_preprocessor
        super().__init__()

    def __iter__(self):
        with gzip.GzipFile(self.source_filepath, 'rU') as in_bz:
            for line in in_bz:
                text = line
                if self.text_preprocessor:
                    text = self.text_preprocessor.preprocess(text)
                tokens = text.split()
                yield tokens
