"""
Module for keep in consistent state mongo data with asterisc data in mysql
"""

import asyncio
from asyncio import ensure_future
from inspect import isclass
from pymongo.errors import PyMongoError
from pymysql.err import MySQLError
from aiomysql.cursors import SSCursor, DictCursor

from .database import DbHelper
from .configuration import config
from .logger import worker as log


def run_workers():
    for worker in _run_each():
        log.info(f"{__name__}.{worker.__name__} was run")


def _run_each():
    """ auto run all subtypes for `Worker` """

    def run(worker):
        ensure_future(worker.run())
        return worker

    return tuple(
        run(worker)
        for worker in globals().values()
        if isclass(worker) and
        issubclass(worker, Worker) and
        worker is not Worker and
        not worker.disabled
    ) if config['worker']['enable'] else ()


class Worker:
    """
    Warning! - all subtypes on auto mode will sheduling, see `run_jobs()`
    """
    disabled = False

    @classmethod
    async def run(cls):
        raise NotImplementedError()

    @classmethod
    async def repeat_action(cls, action, interval=config['worker']['timeoutsec']):
        """
        helper for use in subclases like this:
        `await cls.repeat_action(lambda self: self.sync())`
        """

        self = cls()

        while True:
            try:
                await ensure_future(action(self))
                await asyncio.sleep(interval)
            except (PyMongoError, MySQLError, ValueError) as error:
                log.error(error)


class MongoCdrSyncWorker(Worker):

    def __init__(self):
        self._docslimit = config['worker']['docslimit']
        self._mongocollection = \
            DbHelper.mongo.contactcenter['outbound-postprocessing']
        self._mysql = DbHelper.mysql

    @classmethod
    async def run(cls):
        await cls.repeat_action(lambda self: self._sync())

    async def _sync(self):
        """ sync data for mongo from asterisk """

        futures = ()
        ids = ()

        for userfield, uniqueid in await self._select_cdr(await self._select_mongo()):
            try:
                future = self._mongocollection.update_many(
                    {"callid": uniqueid},
                    {"$set": {"outbound": userfield if userfield else '[CHECKED]'}})

                ids += uniqueid,
                futures += future,

            except (PyMongoError, MySQLError) as error:
                log.error(error)

        if len(ids):
            log.info("run update (%s) documents in outbound: (%s)"
                     % (len(ids), ", ".join(ids)))

        return await asyncio.wait(futures) if len(futures) else None

    async def _select_mongo(self):
        """ take only data where outbound is not set """

        return await self._mongocollection.find({
            "$and": [
                {"callid": {"$exists": True}},
                {"callid": {"$ne": str()}},
                {"callid": {"$ne": None}}
            ],
            "$or": [
                {"outbound": {"$exists": False}},
                {"outbound": {"$eq": str()}},
                {"outbound": {"$eq": None}}
            ]
        }).to_list(self._docslimit)

    def _select_cdr(self, docs=None):
        """
        :rtype: ((userfield, uniqueid), ..., (userfield, uniqueid))
        """

        ids = ",".join("'%s'" % doc['callid'] for doc in docs or [])
        lim = self._docslimit

        return self._mysql(f"""
            SELECT cdr.userfield, cdr.uniqueid FROM cdr
            WHERE cdr.uniqueid IN ({ids}) LIMIT {lim}
        """ if docs else None, SSCursor)


class MongoQueuelogSyncWorker(Worker):

    def __init__(self):
        self._mongocollection = DbHelper.mongo.contactcenter['postprocessing']
        self._docslimit = config['worker']['docslimit']
        self._mysql = DbHelper.mysql

    @classmethod
    async def run(cls):
        await cls.repeat_action(lambda self: self._sync())

    async def _sync(self):

        futures = ()
        ids = ()

        for call in await self._select_queuelog(await self._select_mongo()):
            try:
                call_time, hold_time = self._extract_call_times(call)
                # get just future and run execution
                future = self._mongocollection.update_many(
                    {"callid": call['callid']},
                    {"$set": {"callTime": call_time, "holdTime": hold_time}}
                )

                futures += future,
                ids += call["callid"],

            except (PyMongoError, MySQLError, ValueError) as error:
                log.error(error)

        if len(ids):
            log.info("run update (%s) documents in queue: (%s)"
                     % (len(ids), ", ".join(ids)))

        return await asyncio.wait(futures) if len(futures) else None

    async def _select_mongo(self):
        return await self._mongocollection.find({
            "$and": [
                {"callid": {"$exists": True}},
                {"callid": {"$ne": str()}},
                {"callid": {"$ne": None}}
            ],
            "$or": [
                {"holdTime": {"$exists": False}},
                {"holdTime": {"$eq": str()}},
                {"holdTime": {"$eq": None}},
                {"callTime": {"$exists": False}},
                {"callTime": {"$eq": str()}},
                {"callTime": {"$eq": None}}
            ]
        }).to_list(self._docslimit)

    def _extract_call_times(self, call):

        if 'COMPLETEAGENT' in call['event_concat'] or 'COMPLETECALLER' in call['event_concat']:
            call_time = self._parse_time(call['data2_concat'])
            hold_time = self._parse_time(call['data1_concat'])
        elif 'TRANSFER' in call['event_concat']:
            call_time = self._parse_time(call['data4_concat'])
            hold_time = self._parse_time(call['data3_concat'])
        else:
            call_time = self._parse_time(call['data2_concat'])
            hold_time = self._parse_time(call['data1_concat'])

        return call_time, hold_time

    def _parse_time(self, rawdata, separator=":"):
        """ parse special format :rawdata string from asterisk """

        try:
            minutes, seconds = divmod(int(rawdata.split(separator)[-1]), 60)
            hours, minutes = divmod(minutes, 60)
        except ValueError:
            hours, minutes, seconds = 0, 0, 0

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def _select_queuelog(self, docs=None):

        # extract identity from mongo documents
        ids = ",".join("'%s'" % doc['callid'] for doc in docs or [])
        lim = self._docslimit

        return self._mysql(f"""
            SELECT
            GROUP_CONCAT(data5 ORDER BY id SEPARATOR ':') AS data5_concat,
            GROUP_CONCAT(data4 ORDER BY id SEPARATOR ':') AS data4_concat,
            GROUP_CONCAT(data3 ORDER BY id SEPARATOR ':') AS data3_concat,
            GROUP_CONCAT(data2 ORDER BY id SEPARATOR ':') AS data2_concat,
            GROUP_CONCAT(data1 ORDER BY id SEPARATOR ':') AS data1_concat,
            GROUP_CONCAT(event ORDER BY id SEPARATOR ':') AS event_concat,
            GROUP_CONCAT(agent ORDER BY id SEPARATOR ':') AS agent_concat,
            callid,
            time,
            queuename
            FROM queue_log
            WHERE callid IN ({ids})
            AND (
                event = 'CONNECT' OR
                event = 'COMPLETEAGENT' OR
                event = 'COMPLETECALLER' OR
                event = 'TRANSFER' OR
                event = 'ENTERQUEUE'
            )
            GROUP BY callid
            LIMIT {lim}
        """ if docs else None, DictCursor)
