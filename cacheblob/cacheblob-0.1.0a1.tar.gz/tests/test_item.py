import unittest
import os
import sys

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../src/")))

class TestCacheItem(unittest.TestCase):

    def test_init_both_expiry_duration(self):
        import cacheblob.item as item

        self.assertRaises(
            ValueError,
            item.CacheItem,
            index=1,
            value=1,
            expiry=1,
            duration=1)

    def test_init_wrong_duration_type(self):
        import cacheblob.item as item
        import datetime

        self.assertRaises(
            TypeError,
            item.CacheItem,
            index=1,
            value=1,
            duration=datetime.datetime.now())

    def test_init_wrong_expiry_type(self):
        import cacheblob.item as item

        self.assertRaises(
            TypeError,
            item.CacheItem,
            index=1,
            value=1,
            expiry=1)

    def test_init_wrong_expiry_type2(self):
        import cacheblob.item as item
        import datetime

        self.assertRaises(
            TypeError,
            item.CacheItem,
            index=1,
            value=1,
            expiry=datetime.timedelta(1))

    def test_init_wrong_created_type(self):
        import cacheblob.item as item

        self.assertRaises(
            TypeError,
            item.CacheItem,
            index=1,
            value=1,
            created=1)

    def test_init_wrong_created_type2(self):
        import cacheblob.item as item
        import datetime

        self.assertRaises(
            TypeError,
            item.CacheItem,
            index=1,
            value=1,
            created=datetime.timedelta(1))

    def test_init_past_expiry(self):
        import cacheblob.item as item
        import datetime

        self.assertRaises(ValueError, item.CacheItem, index=1, value=1,
                          expiry=datetime.datetime.now() + datetime.timedelta(-1))

    def test_init_none(self):
        import cacheblob.item as item

        test_item = item.CacheItem(index=1, value=1)
        self.assertEqual(1, test_item.index)

    def test_init_duration(self):
        import cacheblob.item as item
        import datetime

        test_item = item.CacheItem(
            index=1, value=1, duration=datetime.timedelta(10))
        self.assertEqual(datetime.timedelta(10), test_item.duration)

    def test_init_created_and_duration(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()

        test_item = item.CacheItem(
            index=1,
            value=1,
            created=created,
            duration=datetime.timedelta(10))
        self.assertEqual(pytz.utc.localize(created), test_item.created)

    def test_init_expiry(self):
        import cacheblob.item as item
        import datetime
        import pytz

        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(index=1, value=1, expiry=expiry)
        self.assertEqual(pytz.utc.localize(expiry), test_item.expiry)

    def test_init_created_and_expiry(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index=1, value=1, created=created, expiry=expiry)
        self.assertEqual(pytz.utc.localize(created), test_item.created)
        self.assertEqual(pytz.utc.localize(expiry), test_item.expiry)

    def test_get_index(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual('alpha', test_item.index)

    def test_get_value(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual('beta', test_item.value)

    def test_get_created(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(pytz.utc.localize(created), test_item.created)

    def test_get_created_localized(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = pytz.utc.localize(datetime.datetime.now())
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(created, test_item.created)

    def test_get_expiry(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(pytz.utc.localize(expiry), test_item.expiry)

    def test_get_expiry_localized(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()
        expiry = pytz.utc.localize(
            datetime.datetime.now() +
            datetime.timedelta(1))

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(expiry, test_item.expiry)

    def test_get_duration(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(expiry - created, test_item.duration)

    def test_get_length(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value='beta',
            created=created,
            expiry=expiry)
        self.assertEqual(4, test_item.length)

    def test_get_length_none_int(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            created=created,
            expiry=expiry)
        self.assertIsNone(test_item.length)

    def test_set_index(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            created=created,
            expiry=expiry)
        test_item.index = 'gamma'
        self.assertEqual('gamma', test_item.index)

    def test_set_empty_duration(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            created=created,
            expiry=expiry)
        test_item.duration = None
        self.assertIsNone(test_item.duration)

    def test_inititalize_empty_duration(self):
        import cacheblob.item as item
        import cacheblob.constants as C
        import datetime

        created = datetime.datetime.now()

        test_item = item.CacheItem(index='alpha', value=1, created=created)
        self.assertEqual(C.DEFAULT_DURATION, test_item.duration)

    def test_negative_duration(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            created=created,
            duration=datetime.timedelta(1))

        with self.assertRaises(ValueError):
            test_item.duration = datetime.timedelta(-1)

    def test_set_empty_expiry(self):
        import cacheblob.item as item
        import datetime

        created = datetime.datetime.now()
        expiry = datetime.datetime.now() + datetime.timedelta(1)

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            created=created,
            expiry=expiry)
        test_item.expiry = None
        self.assertIsNone(test_item.expiry)

    def test_check_updated(self):
        import cacheblob.item as item
        import datetime
        import pytz

        created = datetime.datetime.now()

        test_item = item.CacheItem(index='alpha', value=1, created=created)
        # Not a very specific test, but more stable than equality or a
        # threshold
        self.assertLessEqual(pytz.utc.localize(created), test_item.updated)

    def test_is_expired_false(self):
        import cacheblob.item as item
        import datetime

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            duration=datetime.timedelta(
                minutes=1))

        self.assertFalse(test_item.is_expired)

    def test_is_expired_true(self):
        import cacheblob.item as item
        import datetime
        import time

        test_item = item.CacheItem(
            index='alpha',
            value=1,
            duration=datetime.timedelta(
                milliseconds=1))

        time.sleep(0.01)
        self.assertTrue(test_item.is_expired)

if __name__ == "__main__":
    unittest.main()
