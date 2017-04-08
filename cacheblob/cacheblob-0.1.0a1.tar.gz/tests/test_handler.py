import unittest
import os
import sys

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../src/")))

class TestBaseHandler(unittest.TestCase):

    def test_init_no_opt(self):
        import cacheblob.handlers.handler as handler

        handler.Handler()

    def test_init_wrong_memoize_max_length_type(self):
        import cacheblob.handlers.handler as handler

        self.assertRaises(
            TypeError, handler.Handler, {
                'memoize_max_length': 'not number'})

    def test_init_wrong_memoize_max_entries_type(self):
        import cacheblob.handlers.handler as handler

        self.assertRaises(
            TypeError, handler.Handler, {
                'memoize_max_entries': 'not number'})

    def test_init_memoize_max_length_and_no_memoize(self):
        import cacheblob.handlers.handler as handler

        self.assertRaises(
            ValueError, handler.Handler, {
                'memoize_max_length': 1000, 'memoize': False})

    def test_init_memoize_max_length(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize_max_length': 1000})
        self.assertEqual(1000, test_handler.memoize_max_length)

    def test_init_memoize_max_entries(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize_max_entries': 1000})
        self.assertEqual(1000, test_handler.memoize_max_entries)

    def test_init_overwrite_true(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'overwrite': 1})
        self.assertTrue(test_handler.overwrite)

    def test_init_overwrite_false(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'overwrite': 0})
        self.assertFalse(test_handler.overwrite)

    def test_init_memoize_true(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize': 1})
        self.assertTrue(test_handler.memoize)

    def test_init_memoize_false(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize': 0})
        self.assertFalse(test_handler.memoize)

    def test_init_may_purge_if_expired_true(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'may_purge_if_expired': 1})
        self.assertTrue(test_handler.may_purge_if_expired)

    def test_init_purge_if_expired_false(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'may_purge_if_expired': 0})
        self.assertFalse(test_handler.may_purge_if_expired)

    def test_init_memoize_max_length_default(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.constants as C

        test_handler = handler.Handler()
        self.assertEqual(C.MEMOIZE_MAX_LENGTH, test_handler.memoize_max_length)

    def test_set_memoize_max_length(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize_max_length': 1000})
        test_handler.memoize_max_length = 2000
        self.assertEqual(2000, test_handler.memoize_max_length)

    def test_set_memoize_max_entries(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize_max_entries': 1000})
        test_handler.memoize_max_entries = 2000
        self.assertEqual(2000, test_handler.memoize_max_entries)

    def test_set_overwrite(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'overwrite': 1})
        test_handler.overwrite = False
        self.assertFalse(test_handler.overwrite)

    def test_set_memoize(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'memoize': 1})
        test_handler.memoize = False
        self.assertFalse(test_handler.memoize)

    def test_set_purge_if_expired(self):
        import cacheblob.handlers.handler as handler

        test_handler = handler.Handler({'may_purge_if_expired': 1})
        test_handler.may_purge_if_expired = False
        self.assertFalse(test_handler.may_purge_if_expired)

    def test_store_not_memoizing(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'memoize': False})
        test_item = item.CacheItem(
            index=1, value=1, duration=datetime.timedelta(10))

        self.assertFalse(test_handler.store(test_item))

    def test_store_too_large(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'memoize_max_length': 1})
        test_item = item.CacheItem(
            index=1, value="bb", duration=datetime.timedelta(10))

        self.assertFalse(test_handler.store(test_item))

    def test_store(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index=1, value=1, duration=datetime.timedelta(10))

        self.assertTrue(test_handler.store(test_item))

    def test_fetch_non_existant(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        self.assertIsNone(test_handler.fetch('index2'))

    def test_fetch_not_memoized(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'memoize': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        self.assertIsNone(test_handler.fetch('index'))

    def test_fetch_expired(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime
        import time

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        test_handler.store(test_item)
        time.sleep(0.01)
        self.assertIsNone(test_handler.fetch('index'))

    def test_fetch(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        self.assertEqual('value', test_handler.fetch('index').value)

    def test_fetch_memoize_max_entries_drops(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler(
            {'memoize': True, 'memoize_max_entries': 1})
        test_item = item.CacheItem(
            index='index1',
            value='value1',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        test_handler.store(test_item2)

        self.assertIsNone(test_handler.fetch(test_item.index))
        self.assertEqual('value2', test_handler.fetch(test_item2.index).value)

    def test_overwrite_true(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'overwrite': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        test_handler.store(test_item2)
        self.assertEqual('value2', test_handler.fetch('index').value)

    def test_overwrite_false(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'overwrite': False})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index',
            value='value2',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        test_handler.store(test_item2)
        self.assertEqual('value', test_handler.fetch('index').value)

    def test_purge(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        test_handler.purge(test_item.index)
        self.assertIsNone(test_handler.fetch('index'))

    def test_purge_not_exists(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        self.assertFalse(test_handler.purge('index2'))

    def test_fetch_all(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler()
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(10))
        test_item2 = item.CacheItem(
            index='index2',
            value='value2',
            duration=datetime.timedelta(10))

        test_handler.store(test_item)
        test_handler.store(test_item2)

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(all_items and len(all_items) == 2)

        if all_items and len(all_items) == 2:
            self.assertEqual(set([test_item.value, test_item2.value]),
                             set([all_items[0].value, all_items[1].value]))

    def test_fetch_all_with_expired(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime
        import time

        test_handler = handler.Handler({'may_purge_if_expired': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        test_handler.store(test_item)

        time.sleep(0.01)

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertEqual([], all_items)

    def test_purge_if_expired(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime
        import time

        test_handler = handler.Handler({'may_purge_if_expired': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                milliseconds=1))

        test_handler.store(test_item)

        time.sleep(0.01)

        status = test_handler.purge_if_expired(test_item.index)

        self.assertTrue(status)

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertEqual([], all_items)

    def test_purge_if_expired_not_expired(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime

        test_handler = handler.Handler({'may_purge_if_expired': True})
        test_item = item.CacheItem(
            index='index',
            value='value',
            duration=datetime.timedelta(
                days=1))

        test_handler.store(test_item)

        status = test_handler.purge_if_expired(test_item.index)

        self.assertFalse(status)

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertEqual(1, len(all_items))

    def test_purge_any_expired_true(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime
        import time

        test_handler = handler.Handler({'may_purge_if_expired': True})
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

        test_handler.store(test_item)
        test_handler.store(test_item2)

        time.sleep(0.01)

        status = test_handler.purge_any_expired()

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

    def test_purge_any_expired_false(self):
        import cacheblob.handlers.handler as handler
        import cacheblob.item as item
        import datetime
        import time

        test_handler = handler.Handler({'may_purge_if_expired': False})
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

        test_handler.store(test_item)
        test_handler.store(test_item2)

        time.sleep(0.01)

        status = test_handler.purge_any_expired()

        all_items = []
        for item in test_handler.fetch_all():
            all_items.append(item)

        self.assertTrue(status)
        self.assertTrue(all_items and len(all_items) == 1)

        if all_items and len(all_items) == 1:
            self.assertEqual(test_item2.value, all_items[0].value)

if __name__ == "__main__":
    unittest.main()
