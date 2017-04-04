from collections import defaultdict
import motor.motor_asyncio
import pymongo
from bson import DBRef
from asynclib.amqp.client import AMQPClient


class Mongo(object):

    def __init__(self, url, name):
        self._client = None
        self.name = name
        self.url = url

    def get_collection(self, collection_name, read_preference):
        if self._client is None:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(self.url)
        return self._client.get_database(self.name, read_preference=read_preference).get_collection(collection_name)


class MongoDBAMQPProxy(object):

    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.amqp_client = AMQPClient(name=db_name)

    def __getattr__(self, item):
        async def query_maker(*args, **kwargs):
            await self.amqp_client.connect()
            result = await self.amqp_client.call('mongo_query', parameters={'method': item,
                                                                            'collection': self.collection_name
                ,'args': args, 'kwargs': kwargs})
            await self.amqp_client.close()
            return result
        return query_maker


class DenormDBProxy(MongoDBAMQPProxy):

    def __init__(self):
        super(DenormDBProxy, self).__init__('denorm', 'ref_map')


class MongoDBManager(object):

    def __init__(self, collection_name, mongo_retriever,
                 read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED):
        self.mongo_retriever = mongo_retriever
        self.read_preference = read_preference
        self.collection_name = collection_name
        self._db = None

    @property
    def db(self) -> motor.motor_asyncio.AsyncIOMotorCollection:
        if self._db is None:
            self._db = self.mongo_retriever.mongo.get_collection(self.collection_name, self.read_preference)
        return self._db

    def __getattr__(self, item):
        #proxy for query
        return getattr(self.db, item)

    async def find_by_id_list(self, id_list):
        return await self.db.find({'$id': {'$in': id_list}})

    async def get_by_id(self, _id):
        return await self.db.find_one({'_id': _id})

    async def _create(self, parameters):
        parameters['_id'] = await self.db.insert_one(parameters).inserted_id
        return parameters

    def cursor_map(self, cursor):
        return {str(i['_id']): i for i in list(cursor)}

    async def update_many_denormalized(self, query, data, *args, **kwargs):
        old_cursor_map = self.cursor_map(self.db.find(query))
        result = await self.db.update_many(query, data, *args, **kwargs)
        if result.modified_count > 0:
            new_cursor = self.db.find(query)
            if new_cursor.count() > 0:
                new_cursor_map = self.cursor_map(new_cursor)
                denorm_db = DenormDBProxy()
                denorm_db.denorm_collection(self, old_cursor_map, new_cursor_map)
        return result

    async def update_one_denormalized(self, query, data, *args, **kwargs):
        doc_before = await self.db.find_one(query)
        doc_after = await self.db.find_one_and_update(
            query, data, return_document=pymongo.ReturnDocument.AFTER, *args, **kwargs
        )
        if doc_after:
            denorm_db = DenormDBProxy()
            denorm_db.denorm(self, doc_after['_id'], doc_before, doc_after)


def cursor_to_result(cursor, skip=None, limit=None):
    """
    :param limit: int
    :param skip: int
    :type cursor: pymongo.Cursor
    """
    try:
        if limit is not None:
            limit = int(limit)
        if skip is not None:
            skip = int(skip)
    except (ValueError, TypeError):
        limit = None
        skip = None
    total = cursor.count()
    if skip is not None:
        cursor.skip(skip)
    if limit is not None:
        cursor.limit(limit)
    return {
        'objects': list(cursor),
        'total': total
    }


def collect_db_ref(items):
    values = []
    if isinstance(items, dict):
        items = items.values()
    for item in items:
        if isinstance(item, DBRef):
            values.append(DBRef(item.collection, item.id, item.database))
            values += collect_db_ref(item._DBRef__kwargs)
        elif isinstance(item, (list, dict)):
            values += collect_db_ref(item)
    return values


def append_db_ref(item, data):
    if isinstance(item, DBRef):
        item._DBRef__kwargs = append_db_ref(item._DBRef__kwargs, data)
        return data[item.database][item.collection].get(item.id) or item
    elif isinstance(item, list):
        return [append_db_ref(i, data) for i in item]
    elif isinstance(item, dict):
        return {k: append_db_ref(i, data) for k, i in item.items()}
    return item


async def deref(data, items):
    refs = defaultdict(list)
    for r in set(collect_db_ref(data)):
        if r.database + '.' + r.collection in items:
            refs[(r.database, r.collection)].append(r.id)
    docs = defaultdict(lambda: defaultdict(dict))
    for key, _id in refs.items():
        docs[key[0]][key[1]] = {i['_id']: i for i in await MongoDBAMQPProxy(key[0], key[1]).find({'_id': {'$in': _id}})}
    return append_db_ref(data, docs)



