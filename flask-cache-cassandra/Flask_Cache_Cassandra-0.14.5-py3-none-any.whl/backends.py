import pickle
from werkzeug.contrib.cache import (BaseCache, NullCache, SimpleCache, MemcachedCache,
                                    GAEMemcachedCache, FileSystemCache)
from ._compat import range_type, PY2


class SASLMemcachedCache(MemcachedCache):

    def __init__(self, servers=None, default_timeout=300, key_prefix=None,
                 username=None, password=None):
        BaseCache.__init__(self, default_timeout)

        if servers is None:
            servers = ['127.0.0.1:11211']

        import pylibmc
        self._client = pylibmc.Client(servers,
                                      username=username,
                                      password=password,
                                      binary=True)

        self.key_prefix = key_prefix


if PY2:
    def dumper(value):
        return bytearray(pickle.dumps(value))
else:
    def dumper(value):
        return pickle.dumps(value)


class CassandraCache(BaseCache):
    """Cassandra flask-cache implementation.

    Initialized with::

        nodes: list of nodes (or None for localhost)
        port: integer port to connect on, default 9042
        keyspace: string keyspace to use, default flask_cache
        table: string table name to use, default flask_cache
        default_timeout: int seconds to cache by default, None == forever
        replication_factor: int number of nodes to replicate data with
        read_consistency: int number of responses to require for reads
        write_consistency: int cassandra.ConsistencyLevel for writes
        delete_consistency: int cassandra.ConsistencyLevel for deletes
        table_consistency: int cassandra.ConsistencyLevel for modifying tables

    Raises:
        ValueError if the keyspace or table are not valid names
    """

    _clusters = {}

    @staticmethod
    def _cluster(nodes, port):
        if (nodes, port) not in CassandraCache._clusters:
            CassandraCache._clusters[(nodes, port)] = Cluster(nodes, port=port)
        return CassandraCache._clusters[(nodes, port)]

    def __init__(self, nodes=None, port=None, keyspace=None,
                 table=None, default_timeout=None,
                 replication_factor=1, read_consistency=1,
                 write_consistency=0, delete_consistency=0,
                 table_consistency=6):

        self.keyspace = keyspace or "flask_cache"
        self.table = table or "flask_cache"

        for char in ("-", " "):
            for name in (self.keyspace, self.table):
                if char in name:
                    raise ValueError("'{}' not valid in {}".format(char, name))

        self.nodes = tuple(nodes or ["localhost"])
        self.port = port or 9042
        self.default_timeout = default_timeout
        self.read_consistency = read_consistency
        self.write_consistency = write_consistency
        self.delete_consistency = delete_consistency
        self.table_consistency = table_consistency

        self.cluster = CassandraCache._cluster(self.nodes, self.port)
        self.cluster.connect().execute(
            """
            CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication =
            {{'class': 'SimpleStrategy', 'replication_factor': {factor}}}
            """.format(keyspace=self.keyspace, factor=replication_factor)
        )
        self.session = self.cluster.connect(keyspace=self.keyspace)
        self._create_table()

    def _execute(self, statement, consistency, parameters=None, results=False):
        """Executes a statement against a cassandra cluster.

        Args::

            statement: string statement to run, using named placeholders
            consistency: int cassandra.ConsistencyLevel to use
            parameters: dict or tuple of values to insert into the statement
            results: boolean to return the cassandra.cluster.ResultSet as well
        """

        res = self.session.execute(
            SimpleStatement(statement, consistency_level=consistency),
            parameters=parameters,
        )
        try:
            res.response_future.result()  # force this thread to wait
        except:
            success = False
        else:
            success = True
        finally:
            if results:
                return success, res
            else:
                return success

    def _create_table(self, consistency=None):
        """Creates the table for our cache."""

        if consistency is None:
            consistency = self.table_consistency

        return self._execute(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                key text PRIMARY KEY,
                value blob,
            )
            """.format(table=self.table),
            consistency,
        )

    def add(self, key, value, timeout=None, consistency=None):
        """Adds a key/value to the cache for timeout seconds.

        Args::

            key: string key name
            value: object value to store
            timeout: int seconds to cache for, or self.default_timeout, or None
            consistency: int ConsistencyLevel, or self.write_consistency

        Returns:
            False if the key is already known, True on success
        """

        if self.has(key):
            return False
        else:
            return self.set(key, value, timeout, consistency)

    def clear(self, consistency=None):
        """Clears the cache by dropping the table and recreating it."""

        if consistency is None:
            consistency = self.table_consistency

        success = self._execute(
            "DROP TABLE {}".format(self.table),
            consistency,
        )
        if success:
            success = self._create_table(consistency)
        return success

    def dec(self, key, delta=1):
        """Decrement a counter in the cache, by delta."""

        new_value = (self.get(key) or 0) - delta
        return new_value if self.set(key, new_value) else False

    def inc(self, key, delta=1):
        """Increment a counter in the cache, by delta."""

        new_value = (self.get(key) or 0) + delta
        return new_value if self.set(key, new_value) else False

    def delete(self, key, consistency=None):
        """Deletes a key from the cache.

        Args:
            key: string key to delete
            consistency: int ConsistencyLevel, or self.delete_consistency

        Returns:
            boolean of success
        """

        if consistency is None:
            consistency = self.delete_consistency

        return self._execute(
            """
            DELETE FROM {table} WHERE key = %(key)s
            """.format(table=self.table),
            consistency,
            {"key": key},
        )

    def get(self, key, consistency=None):
        """Returns the python object cached for the key, or None.

        Args:
            key: string key to retrieve
            consistency: int ConsistencyLevel, or self.read_consistency
        """

        if consistency is None:
            consistency = self.read_consistency

        success, rows = self._execute(
            """
            SELECT value FROM {table} WHERE key = %(key)s LIMIT 1
            """.format(table=self.table),
            consistency,
            {"key": key},
            results=True,
        )

        if not success:
            return

        for value in rows:
            return pickle.loads(value.value)

    def has(self, key, consistency=None):
        """Returns a boolean of if the key is known.

        Args:
            key: string key to search for
            consistency: int ConsistencyLevel, or self.read_consistency
        """

        if consistency is None:
            consistency = self.read_consistency

        success, rows = self._execute(
            """
            SELECT value FROM {table} WHERE key = %(key)s LIMIT 1
            """.format(table=self.table),
            consistency,
            {"key": key},
            results=True,
        )

        if not success:
            return False

        for value in rows:
            return True

        return False

    def set(self, key, value, timeout=None, consistency=None):
        """Stores a python object in cassandra.

        Args:
            key: string key to reference the value by
            value: python object to store
            timeout: int seconds (or None for forever) to cache for
            consistency: int ConsistencyLevel or self.write_consistency

        Returns:
            boolean of success
        """

        if consistency is None:
            consistency = self.write_consistency

        timeout = timeout or self.default_timeout
        if timeout:
            success = self._execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                USING TTL {timeout}
                """.format(table=self.table, timeout=timeout),
                consistency,
                {"key": key, "value": dumper(value)}
            )
        else:
            success = self._execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                """.format(table=self.table),
                consistency,
                {"key": key, "value": dumper(value)}
            )

        return success


def null(app, config, args, kwargs):
    return NullCache()


def simple(app, config, args, kwargs):
    kwargs.update(dict(threshold=config['CACHE_THRESHOLD']))
    return SimpleCache(*args, **kwargs)


def memcached(app, config, args, kwargs):
    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(key_prefix=config['CACHE_KEY_PREFIX']))
    return MemcachedCache(*args, **kwargs)


def saslmemcached(app, config, args, kwargs):
    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(username=config['CACHE_MEMCACHED_USERNAME'],
                       password=config['CACHE_MEMCACHED_PASSWORD'],
                       key_prefix=config['CACHE_KEY_PREFIX']))
    return SASLMemcachedCache(*args, **kwargs)


def gaememcached(app, config, args, kwargs):
    kwargs.update(dict(key_prefix=config['CACHE_KEY_PREFIX']))
    return GAEMemcachedCache(*args, **kwargs)


def filesystem(app, config, args, kwargs):
    args.insert(0, config['CACHE_DIR'])
    kwargs.update(dict(threshold=config['CACHE_THRESHOLD']))
    return FileSystemCache(*args, **kwargs)


# RedisCache is supported since Werkzeug 0.7.
try:
    from werkzeug.contrib.cache import RedisCache
    from redis import from_url as redis_from_url
except ImportError:
    pass
else:
    def redis(app, config, args, kwargs):
        kwargs.update(dict(
            host=config.get('CACHE_REDIS_HOST', 'localhost'),
            port=config.get('CACHE_REDIS_PORT', 6379),
        ))
        password = config.get('CACHE_REDIS_PASSWORD')
        if password:
            kwargs['password'] = password

        key_prefix = config.get('CACHE_KEY_PREFIX')
        if key_prefix:
            kwargs['key_prefix'] = key_prefix

        db_number = config.get('CACHE_REDIS_DB')
        if db_number:
            kwargs['db'] = db_number

        redis_url = config.get('CACHE_REDIS_URL')
        if redis_url:
            kwargs['host'] = redis_from_url(
                redis_url,
                db=kwargs.pop('db', None),
            )

        return RedisCache(*args, **kwargs)


# Cassandra cache introduced in flask-cache 0.14
try:
    from cassandra.cluster import Cluster
    from cassandra.query import SimpleStatement
except ImportError:
    pass
else:
    def cassandra(app, config, args, kwargs):
        kwargs.update(dict(
            nodes=config.get('CACHE_CASSANDRA_NODES'),
            port=config.get('CACHE_CASSANDRA_PORT'),
            table=config.get('CACHE_CASSANDRA_TABLE'),
            keyspace=config.get('CACHE_CASSANDRA_KEYSPACE'),
            replication_factor=config.get('CACHE_CASSANDRA_REPLICATION_FACTOR'),
            read_consistency=config.get('CACHE_CASSANDRA_READ_CONSISTENCY'),
            write_consistency=config.get('CACHE_CASSANDRA_WRITE_CONSISTENCY'),
            delete_consistency=config.get('CACHE_CASSANDRA_DELETE_CONSISTENCY'),
            table_consistency=config.get('CACHE_CASSANDRA_TABLE_CONSISTENCY'),
        ))

        return CassandraCache(*args, **kwargs)


class SpreadSASLMemcachedCache(SASLMemcachedCache):
    """
    Simple Subclass of SASLMemcached client that spread value across multiple
    key is they are bigger than a given treshhold.

    Spreading require using pickle to store the value, wich can significantly
    impact the performances.
    """

    def __init__(self, *args, **kwargs):
        """
        chunksize : (int) max size in bytes of chunk stored in memcached
        """
        self.chunksize = kwargs.get('chunksize', 950000)
        self.maxchunk = kwargs.get('maxchunk', 32)
        super(SpreadSASLMemcachedCache, self).__init__(*args, **kwargs)

    def delete(self, key):
        for skey in self._genkeys(key):
            super(SpreadSASLMemcachedCache, self).delete(skey)

    def set(self, key, value, timeout=None, chunk=True):
        """set a value in cache, potentially spreding it across multiple key.

        chunk : (Bool) if set to false, does not try to spread across multiple key.
                this can be faster, but will fail if value is bigger than chunks,
                and require you to get back the object by specifying that it is not spread.

        """
        if chunk:
            return self._set(key, value, timeout=timeout)
        else:
            return super(SpreadSASLMemcachedCache, self).set(key, value, timeout=timeout)

    def _set(self, key, value, timeout=None):
        # pickling/unpickling add an overhed,
        # I didn't found a good way to avoid pickling/unpickling if
        # key is smaller than chunksize, because in case or <werkzeug.requests>
        # getting the length consume the data iterator.
        serialized = pickle.dumps(value, 2)
        values = {}
        len_ser = len(serialized)
        chks = range_type(0, len_ser, self.chunksize)
        if len(chks) > self.maxchunk:
            raise ValueError('Cannot store value in less than %s keys' % (self.maxchunk))
        for i in chks:
            values['%s.%s' % (key, i // self.chunksize)] = serialized[i:i + self.chunksize]
        super(SpreadSASLMemcachedCache, self).set_many(values, timeout)

    def get(self, key, chunk=True):
        """get a value in cache, potentially spreded it across multiple key.

        chunk : (Bool) if set to false, get a value set with set(..., chunk=False)
        """
        if chunk:
            return self._get(key)
        else:
            return super(SpreadSASLMemcachedCache, self).get(key)

    def _genkeys(self, key):
        return ['%s.%s' % (key, i) for i in range_type(self.maxchunk)]

    def _get(self, key):
        to_get = ['%s.%s' % (key, i) for i in range_type(self.maxchunk)]
        result = super(SpreadSASLMemcachedCache, self).get_many(*to_get)
        serialized = ''.join([v for v in result if v is not None])
        if not serialized:
            return None
        return pickle.loads(serialized)


def spreadsaslmemcachedcache(app, config, args, kwargs):

    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(username=config.get('CACHE_MEMCACHED_USERNAME'),
                       password=config.get('CACHE_MEMCACHED_PASSWORD'),
                       key_prefix=config.get('CACHE_KEY_PREFIX')))
    return SpreadSASLMemcachedCache(*args, **kwargs)
