import logging

_log = logging.getLogger(__name__)


def create_db():
  import redis
  import phovea_server.config

  c = phovea_server.config.view('phovea_data_redis.mapping')

  # print c.hostname, c.port, c.db
  return redis.Redis(host=c.hostname, port=c.port, db=c.db)


class RedisMappingTable(object):
  def __init__(self, from_idtype, to_idtype):
    self.from_idtype = from_idtype
    self.to_idtype = to_idtype

  def __call__(self, ids):
    db = create_db()

    def map_impl(id):
      key = '{}2{}.{}'.format(self.from_idtype, self.to_idtype, id)
      v = db.get(key) or ''
      return v.split(';')

    return [map_impl(id) for id in ids]


def _discover_mappings():
  db = create_db()
  mappings = db.get('mappings')
  _log.info('found %s', mappings)
  if not mappings:
    return
  mappings = [r for r in mappings.split(';') if r.strip()]
  for key in mappings:
    parts = key.split('2')
    _log.info('loading redis mapping table from %s to %s', parts[0], parts[1])
    yield RedisMappingTable(parts[0], parts[1])


class RedisMappingProvider(object):
  def __init__(self):
    self._mappings = list(_discover_mappings())

  def __iter__(self):
    return iter(((f.from_idtype, f.to_idtype, f) for f in self._mappings))


def create():
  return RedisMappingProvider()
