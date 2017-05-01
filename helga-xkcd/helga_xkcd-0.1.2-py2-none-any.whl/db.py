import random

import pymongo

from helga import log
from helga import settings
from helga.db import db

from twisted.internet import reactor

from helga_xkcd.client import XKCDClient

logger = log.getLogger(__name__)

MAX_SYNCHRONOUS = getattr(settings, 'XKCD_MAX_SYNCHRONOUS_REQS', 10)


def fetch_latest_comic():
    cl = XKCDClient()
    latest = cl.fetch_latest()
    db_latest = newest() or 0
    if latest['num'] > db_latest:
        logger.debug('Newer comics exist, filling in gaps!')
        reactor.callLater(0, refresh_db, latest['num'], (db_latest + 1))
    return latest


def fetch_comic_number(number):
    return db.xkcd.find_one({'num': number})


def fetch_random_comic():
    numbers = [doc['num'] for doc in db.xkcd.find({}, {'num': 1, '_id': 0})]
    if numbers:
        return db.xkcd.find_one({'num': random.choice(numbers)})
    return None


def fetch_and_store(comic_number):
    """ if comic is not present, stores it. If it is, overwrites it"""
    xkcd_client = XKCDClient()
    try:
        comic = xkcd_client.fetch_number(comic_number)
        db.xkcd.replace_one({'num': comic['num']}, comic, upsert=True)
    except pymongo.errors.PyMongoError:
        logger.exception('Error inserting comic %d into database. You might get strange behavior.', comic_number)


def newest():
    newest_in_db = db.xkcd.find_one(sort=[('num', pymongo.DESCENDING)])
    if newest_in_db:
        return newest_in_db['num']
    return None


def oldest():
    first = db.xkcd.find_one(sort=[('num', pymongo.ASCENDING)])
    if first:
        return first['num']
    return None


def fetch_comic_about(text):
    return db.xkcd.find_one({'$text': {'$search': text}}, {'score': {'$meta': 'textScore'}}, sort=[('score', {'$meta': 'textScore'})])


def init_db():
    """ setup indexes for text search

    should only be called when the plugin is first installed and configured
    """
    logger.debug('Initializing database indexes')
    definitions = [
        [('num', pymongo.DESCENDING)],
        [('$**', pymongo.TEXT)]
    ]
    for index_def in definitions:
        kwargs = dict(background=True)
        if index_def[0][0] == 'num':
            kwargs.update({'unique': True})
        try:
            db.xkcd.create_index(index_def, **kwargs)
        except pymongo.errors.DuplicateKeyError:
            logger.debug('Index already exists:(%s), skipping', index_def)


def get_db_id_gaps():

    """ returns the maximum stored id and the maximum remote id """
    if db is None:  # pragma: no cover
        logger.warning('Cannot ensure xkcd database is up to date. No database connection')
        return None, None

    init_db()
    xkcd_client = XKCDClient()
    max_local_id = newest() or 1
    logger.debug('Max comic id in database: %d', max_local_id)
    max_remote_id = xkcd_client.fetch_latest().get('num')
    logger.debug('Max comic id on site: %d', max_remote_id)
    return max_remote_id, max_local_id


def refresh_db(high_id, low_id):
    """
    Refreshes the database by filling in all the comic IDs between high_id and low_id.

    assumes that high_id > low_id.
    """
    if high_id <= low_id:
        logger.debug('No work to (%s -> %s). Skipping database refresh', high_id, low_id)
        return

    # partition high -> low in max_sync size chunks
    if (high_id - low_id) > MAX_SYNCHRONOUS:
        logger.debug('Too many missing comics. Chunking and populating asynchronously')
        old_high = high_id
        new_high = max(high_id - MAX_SYNCHRONOUS, 1)
        jitter = random.random()
        reactor.callLater(jitter, refresh_db, old_high, new_high)
        reactor.callLater(jitter, refresh_db, new_high - 1, low_id)
        return

    logger.debug('Fetching comics from high_id %s to low_id %s', high_id, low_id)
    for comic_number in xrange(high_id, low_id - 1, -1):
        fetch_and_store(comic_number)


def populate_db():
    """ Populates the database with comics fetched from xkcd API

    Makes some assumptions about the state of the database. Assumed to have either:
        a) no data in it at all.
        b) all of the comics from min(doc['num'] for doc in db.xkcd.find()) to max(doc['num'] for doc in db.xkcd.find())

    In the former case, it will get the latest comic from the API, and add each number from that comics id to 1
    In the later case, it will get the max stored comic, and the max site comic, and fill them in by counting down
    """
    max_remote, max_local = get_db_id_gaps()
    if max_remote and max_local:
        refresh_db(max_remote, max_local)
    else:
        msg = (
            'Unable to get max_remote (%s) or max_local (%s) ids.'
            'Skipping db population for now'
        )
        logger.debug(msg, max_remote, max_local)
