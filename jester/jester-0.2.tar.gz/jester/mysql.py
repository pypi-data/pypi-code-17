import json
from jester.constants import *
from nmi_mysql import nmi_mysql
import jester.utils

class Query:
    def __init__(self, query, params=None, schema=None):
        """
        :param query: Query string with formats
        :type query: String

        :param params: Escape params
        :type params: Dict

        :param schema: Column schema
        :type schema:
        """
        self.query = query
        self.params = params
        self.schema = schema

class MySQLConnection:

    def __init__(self, host, port, username, password, database):
        conf = {
            'host': host,
            'user': username,
            'password': password,
            'db': database,
            'port': port,
            'max_pool_size': 20  # optional, default is 10
        }

        self.db = nmi_mysql.DB(conf)

    def execute(self, query):
        rows = self.execute_raw(query.query, query.params)
        if query.schema is None: return rows
        self._apply_schema(rows, query)
        return rows

    def execute_raw(self, query, params=None):
        if params is None:
            params = []
        return self.db.query(query, params)

    def execute_batch_insert(self, query, params, size=100):
        results = []
        for chunk in bard.utils.chunk(params, size):
            results.append(self.execute_raw(query, list(chunk)))

        return results

    def execute_batch_update(self, query, params, size=100):
        if len(params) > 1:
            raise Exception("This function does not support this form of update!")

        ids = params[0]

        results = []
        for chunk in bard.utils.chunk(ids, size):
            results.append(self.execute_raw(query, [list(chunk)]))

        return results

    def _apply_schema(self, rows, query):
        for row in rows:
            for key, _type in query.schema.items():
                if row[key] is not None:
                    try:
                        if _type == JSON:
                            try:
                                row[key] = json.loads(row[key])
                            except:
                                row[key] = None
                        elif _type == STR:
                            row[key] = str(row[key])
                        elif _type == INT:
                            row[key] = int(row[key])
                        elif _type == FLOAT:
                            row[key] = float(row[key])
                        elif _type == BOOL:
                            row[key] = bool(row[key])
                    except Exception as e:
                        print("Exception parsing %s on value %s" % (key, row[key]))
                        raise e