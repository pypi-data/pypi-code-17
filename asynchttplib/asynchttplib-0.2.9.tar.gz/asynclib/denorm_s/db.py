import flatdict
import pymongo
from bson import DBRef

from asynclib.database.mongo import MongoDBAMQPProxy, MongoDBManager
from asynclib.utils.functions import get_from_dict


class DenormDBManager(MongoDBManager):

    def __init__(self, mongo):
        super(DenormDBManager, self).__init__('sys', 'denorm', mongo)

    async def create_indexes(self):
        await self.db.create_indexes([
            ('db_name', pymongo.ASCENDING),
            ('collection_name', pymongo.ASCENDING),
            ('ref_id', pymongo.ASCENDING)
        ], background=True, name='denorm')

    async def create(self, loader, callback):
        if loader.extra is not None:
            for _id in loader._id_list if hasattr(loader, '_id_list') else [loader._id]:
                data = {
                    '$set': {
                        'db_name': loader.db_name,
                        'collection_name': loader.collection_name,
                        'ref_id': _id
                    },
                    '$addToSet': {
                        'callback': {
                            'db_name': callback.db_name,
                            'collection_name': callback.collection_name,
                            'extra': loader.extra,
                            'query_path': callback.query_path,
                            'set_path': callback.set_path,
                            'query': callback.query
                        }
                    }
                }
                await self.db.update_one({
                    'db_name': loader.db_name,
                    'collection_name': loader.collection_name,
                    'ref_id': _id}, data, upsert=True)

    async def denorm_collection(self, db, old_map, new_map):
        for key, value in new_map.items():
            await self.denorm(db, value['_id'], old_map[key], value)

    async def denorm(self, db, _id, old, new):
        denorm_pack = self.db.find_one({'db_name': db.db_name, 'collection_name': db.collection_name, 'ref_id': _id})
        if denorm_pack is None:
            return
        denorm_items = [i for i in denorm_pack.get('callback', []) if
                        (i.get('extra') is not None and i.get('db_name') is not None)]
        keys_for_check = self.get_keys_for_check(denorm_items)
        updated_keys = self.get_updated_keys(old, new, keys_for_check)
        for denorm_item in denorm_items:
            extra_keys = denorm_item.get('extra')
            if not self.any_in_array(extra_keys, updated_keys):
                continue
            item = new
            extra = self.prepare_extra(item, denorm_item.get('extra'))
            item = DBRef(
                db.collection_name, _id, db.db_name, _extra=extra
            )
            ref_db = MongoDBAMQPProxy(
                db_name=denorm_item.get('db_name'),
                collection_name=denorm_item.get('collection_name'),
            )
            query = {denorm_item.get('query_path', '') + '.$id': _id}
            if denorm_item.get('query'):
                query.update(denorm_item.get('query'))
            await ref_db.update_many_denormalized(
                query,
                {'$set': {denorm_item.get('set_path'): item}}
            )

    def get_keys_for_check(self, items):
        return set([keypath for item in items for keypath in item.get('extra')])

    def get_updated_keys(self, old, new, keys_for_check):
        updated_keys = []
        for key in keys_for_check:
            if get_from_dict(old, key) != get_from_dict(new, key):
                updated_keys.append(key)
        return updated_keys

    def any_in_array(self, array1, array2):
        return len(set(array2).intersection(set(array1))) > 0

    def prepare_extra(self, item, fields):
        extra = flatdict.FlatDict({}, delimiter='.')
        item = flatdict.FlatDict(item, delimiter='.')
        for key in fields:
            extra[key] = item.get(key)
        extra = extra.as_dict()
        return extra
