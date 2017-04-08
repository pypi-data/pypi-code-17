import unittest
import pymongo
import os
import sys

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../src/")))

class TestMongoHandler(unittest.TestCase):

    TEST_INDEX_FILE = 'tmp.db'

    def setUp(self):
        self.test_handler = None

        c = pymongo.MongoClient()
        c.cacheblob.cache.drop()

    def tearDown(self):
        if self.test_handler is not None:
            self.test_handler.close()

        client = pymongo.MongoClient()
        client.cacheblob.cache.drop()

    def test_init_no_opt(self):
        import cacheblob.handlers.mongo as handler

        handler.Mongo()

    def test_init_wrong_memoize_max_length_type(self):
        import cacheblob.handlers.mongo as handler

        self.assertRaises(
            TypeError, handler.Mongo, {
                'memoize_max_length': 'not number'})

    def test_init_memoize_max_length_and_no_memoize(self):
        import cacheblob.handlers.mongo as handler

        self.assertRaises(
            ValueError, handler.Mongo, {
                'memoize_max_length': 1000, 'memoize': False})

    def test_init_memoize_max_length(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'memoize_max_length': 1000})
        self.assertEqual(1000, self.test_handler.memoize_max_length)

    def test_init_overwrite_true(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'overwrite': 1})
        self.assertTrue(self.test_handler.overwrite)

    def test_init_overwrite_false(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'overwrite': 0})
        self.assertFalse(self.test_handler.overwrite)

    def test_init_memoize_true(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'memoize': 1})
        self.assertTrue(self.test_handler.memoize)

    def test_init_memoize_false(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'memoize': 0})
        self.assertFalse(self.test_handler.memoize)

    def test_init_may_purge_if_expired_true(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'may_purge_if_expired': 1})
        self.assertTrue(self.test_handler.may_purge_if_expired)

    def test_init_may_purge_if_expired_false(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'may_purge_if_expired': 0})
        self.assertFalse(self.test_handler.may_purge_if_expired)

    def test_init_memoize_max_length_default(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.constants as C

        self.test_handler = handler.Mongo()
        self.assertEqual(
            C.MEMOIZE_MAX_LENGTH,
            self.test_handler.memoize_max_length)

    def test_set_memoize_max_length(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'memoize_max_length': 1000})
        self.test_handler.memoize_max_length = 2000
        self.assertEqual(2000, self.test_handler.memoize_max_length)

    def test_set_overwrite(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'overwrite': 1})
        self.test_handler.overwrite = False
        self.assertFalse(self.test_handler.overwrite)

    def test_set_memoize(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'memoize': 1})
        self.test_handler.memoize = False
        self.assertFalse(self.test_handler.memoize)

    def test_set_may_purge_if_expired(self):
        import cacheblob.handlers.mongo as handler

        self.test_handler = handler.Mongo({'may_purge_if_expired': 1})
        self.test_handler.may_purge_if_expired = False
        self.assertFalse(self.test_handler.may_purge_if_expired)

    def test_store(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index=1, value=1, duration=datetime.timedelta(10))

        result = self.test_handler.store(test_item)
        self.assertTrue(result)

    def test_fetch_non_existant(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        result = self.test_handler.fetch('index2')
        self.assertIsNone(result)

    def test_fetch_expired(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        self.test_handler.store(test_item)
        time.sleep(0.01)
        result = self.test_handler.fetch('index')
        self.assertIsNone(result)

    def test_fetch(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        result = self.test_handler.fetch('index').value
        self.assertEqual('value', result)

    def test_fetch_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        fetch = self.test_handler.fetch('index')
        self.assertTrue(fetch is not None)
        result = fetch.value
        self.assertEqual('value', result)

    def test_overwrite_true(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'overwrite': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)
        result = self.test_handler.fetch('index').value
        self.assertEqual('value2', result)

    def test_overwrite_true_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo(
            {'overwrite': True, 'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)
        result = self.test_handler.fetch('index').value
        self.assertEqual('value2', result)

    def test_overwrite_false(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'overwrite': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)
        result = self.test_handler.fetch('index').value
        self.assertEqual('value', result)

    def test_overwrite_false_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo(
            {'overwrite': False, 'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)
        result = self.test_handler.fetch('index').value
        self.assertEqual('value', result)

    def test_purge(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.purge(test_item.index)
        result = self.test_handler.fetch('index')
        self.assertIsNone(result)

    def test_purge_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.purge(test_item.index)
        result = self.test_handler.fetch('index')
        self.assertIsNone(result)

    def test_purge_not_exists(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        result = self.test_handler.purge('index2')
        self.assertFalse(result)

    def test_purge_not_exists_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        result = self.test_handler.purge('index2')
        self.assertFalse(result)

    def test_fetch_all(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(all_items and len(all_items) == 2)

        if all_items and len(all_items) == 2:
            self.assertEqual(set([test_item.value, test_item2.value]),
                             set([all_items[0].value, all_items[1].value]))

    def test_fetch_all_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime

        self.test_handler = handler.Mongo({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(all_items and len(all_items) == 2)

        if all_items and len(all_items) == 2:
            self.assertEqual(set([test_item.value, test_item2.value]),
                             set([all_items[0].value, all_items[1].value]))

    def test_fetch_all_with_expired(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(milliseconds=1))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        time.sleep(0.01)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

    def test_fetch_all_with_expired_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(milliseconds=1))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        time.sleep(0.01)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

    def test_purge_if_expired_true(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo({'may_purge_if_expired': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        self.test_handler.store(test_item)

        time.sleep(0.01)

        status = self.test_handler.purge_if_expired(test_item.index)
        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertEqual([], all_items)

    def test_purge_if_expired_true_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo(
            {'may_purge_if_expired': True, 'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        self.test_handler.store(test_item)

        time.sleep(0.01)

        status = self.test_handler.purge_if_expired(test_item.index)
        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertEqual([], all_items)

    def test_purge_if_expired_false(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo({'may_purge_if_expired': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        self.test_handler.store(test_item)

        time.sleep(0.01)

        status = self.test_handler.purge_if_expired(test_item.index)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertEqual([], all_items)

    def test_purge_if_expired_false_no_memoize(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo(
            {'may_purge_if_expired': False, 'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        self.test_handler.store(test_item)

        time.sleep(0.01)

        status = self.test_handler.purge_if_expired(test_item.index)

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertEqual(0, len(all_items))

    def test_purge_any_expired_true(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo({'may_purge_if_expired': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(
                days=1))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        time.sleep(0.01)

        status = self.test_handler.purge_any_expired()

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

    def test_purge_any_expired_false(self):
        import cacheblob.handlers.mongo as handler
        import cacheblob.item as item
        import datetime
        import time

        self.test_handler = handler.Mongo({'may_purge_if_expired': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(
                days=1))

        self.test_handler.store(test_item)
        self.test_handler.store(test_item2)

        time.sleep(0.01)

        status = self.test_handler.purge_any_expired()

        all_items = []
        for item in self.test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

    """
    """

if __name__ == "__main__":
    unittest.main()
