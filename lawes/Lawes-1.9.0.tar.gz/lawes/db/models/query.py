# -*- coding:utf-8 -*-

from pymongo import MongoClient
from lawes.core.exceptions import MultipleObjectsReturned
from lawes.core.exceptions import DoesNotExist
from lawes.core.exceptions import UniqueError
from lawes.core.exceptions import MongoClientError
from pymongo.errors import OperationFailure

CONF_RAESE = """

The correct formal is:
from lawes.db import models
models.setup(conf={'mongo_uri': 'mongodb://127.0.0.1:27017/test', 'db_name': 'testindex'})
self._mongo: %s , self._db: %s
"""

class ConfigQuerySet(object):


    def __init__(self):
        self.mongo = None
        self.db_name = ''


    def _setup(self, conf):
        """ 设置mongodb的连接方式
        """
        if self.mongo:
            return
        if self.db_name:
            return
        if not 'db_name' in conf:
            raise MongoClientError(CONF_RAESE % ('', ''))
        if not 'mongo_uri' in conf:
            raise MongoClientError(CONF_RAESE % ('', ''))
        self.mongo = MongoClient(conf['mongo_uri'])
        self.db_name = conf['db_name'].lower()

# init the MongoClient
configqueryset = ConfigQuerySet()


class QuerySet(object):


    def __init__(self, model=None):
        self.model = model
        self._mongo = configqueryset.mongo
        self._db = configqueryset.db_name        # the name of the db
        self.db_table = model._meta.db_table      # the name of the collection
        if not self._mongo or not self._db:
            raise MongoClientError(CONF_RAESE % (str(self._mongo), str(self._db)))
        self._collection = getattr(self._mongo[self._db], self.db_table)
        self.filter_query = {}                      # using for Model.objects.filter(filter_query)
        self.order_by_query = ()                    # using for Model.objects.order_by(filter_query)
        self.skip = None                            # using for Model.objects.skip(skip)
        self.limit = None                           # using for Model.objects.limit(limit)


    def __iter__(self):
        for data in self._fetch_all():
            yield data


    def __getitem__(self, item):

        if isinstance(item, int):
            self.limit = item
        elif isinstance(item, slice):
            self.skip = item.start
            self.limit = item.stop - item.start
        return self.__iter__()


    def filter(self, **query):
        self.filter_query.update(query)
        return self


    def _fetch_all(self):
        """ run the sql actually
        :return:
        """
        multi_data = self._collection.find(self.filter_query)
        # order by query
        if self.order_by_query:
            multi_data = multi_data.sort(*self.order_by_query)

        if not self.skip is None:
            multi_data = multi_data.skip(self.skip)
        if not self.limit is None:
            multi_data = multi_data.limit(self.limit)

        for data in multi_data:
            obj = self.model()
            obj = obj.to_obj(data=data)
            yield obj


    def _insert(self, data):
        """
        Inserts a new record for the given model. This provides an interface to
        the InsertQuery class and is how Model.save() is implemented.
        """
        return self._collection.insert(data)


    def _update(self, data):
        """
        Inserts a new record for the given model. This provides an interface to
        the InsertQuery class and is how Model.save() is implemented.
        """
        mongodb_id = data.pop('_id')
        return self._collection.update({'_id': mongodb_id}, {'$set': data}, upsert=True)


    def init_index(self):
        """  create the index_1
        :param db_indexs: {'name': {'unique': False}}
        :return:
        """
        db_indexs = self.model._meta.db_indexs
        try:
            old_index = self._collection.index_information()
        except OperationFailure:
            old_index = {}

        for attr in db_indexs:
            unique = db_indexs[attr].get('unique', False)
            if not attr + '_1' in old_index:
                if unique is True:
                    self._collection.ensure_index(attr, unique=True)
                else:
                    self._collection.ensure_index(attr)
            elif unique is True:
                if not 'unique' in old_index[attr + '_1']:
                    self._collection.ensure_index(attr, unique=True)


    def get(self, *args, **kwargs):
        """
        Performs the query and returns a single object matching the given
        keyword arguments.
        """
        self.filter_query.update(kwargs)
        data = self._collection.find(self.filter_query)
        num = data.count()
        if num == 1:
            obj = self.model()
            obj = obj.to_obj(data=data[0])
            return obj
        if not num:
            raise DoesNotExist(
                "%s matching query does not exist." %
                self.filter_query
            )
        raise MultipleObjectsReturned(
            "findone  %s returned more than one -- it returned %s!" %
            (self.filter_query, num)
        )


    def get_or_create(self, **kwargs):
        """
        :param kwargs:  name='x'
        :return:  a tuple of (object, created), where created is a boolean
        specifying whether an object was created.
        """
        created = False
        try:
            index_information = self._collection.index_information()
        except OperationFailure:
            index_information = {}

        kwargs_keys = set(kwargs.keys())
        index_keys = [ filed for filed in index_information if index_information[filed].get('unique', False)]
        index_keys = [ index_key.replace('_1', '').replace('_-1', '') for index_key in index_keys ]
        need_index_set = kwargs_keys - set(index_keys)
        if need_index_set:
            raise UniqueError('UNIQUE constraint failed: %s: %s, please do collection.ensure_index' % (
            self.db_table, str(need_index_set)))
        self.filter_query.update(kwargs)
        data = self._collection.find(self.filter_query)
        num = data.count()
        if num == 1:
            to_obj_data = data[0]
        elif not num:
            to_obj_data = kwargs
            created = True
        else:
            raise MultipleObjectsReturned(
                "findone  %s returned more than one -- it returned %s!" %
                (self.filter_query, num)
            )

        obj = self.model()
        obj = obj.to_obj(data=to_obj_data)
        if not num:
            obj.save()
        return obj, created


    def all(self):
        self.filter_query = {}
        return self


    def order_by(self, *field_names):
        field_names = field_names[0]
        if '-' in field_names:
            field_names = field_names.replace('-', '')
            order_index = -1
        else:
            order_index = 1
        self.order_by_query = (field_names, order_index)
        return self


