from dbs import getDBs, getDBsFromFile
import jaydebeapi


class jdbc(object):
    def getConn(self):
        if 'dbconffile' in dir(self):
            dbs = getDBsFromFile(self.dbconffile)
        else:
            dbs = getDBs()

        if self.db in dbs.keys():
            conn = jaydebeapi.connect(dbs[self.db]['jdbc_driver'],
                    dbs[self.db]['jdbc_url'],
                    jars=dbs[self.db]['jars'],
                    props=dbs[self.db]['props']
                    )
            return conn.cursor()
        else:
            raise Exception('Can not find db "%s"' % self.db)

    def query(self, params):
        if len(params) != len(self.params):
            print "Wrong Args"
            print self.params
        else:
            conn = self.getConn()
            query_dict = {}
            for i in range(len(self.params)):
                query_dict[self.params[i]] = params[i]
            conn.execute(self.q.format(**query_dict))
            result = conn.fetchall()

            lines = []
            if result is not None:
                if isinstance(result, basestring):
                    print result

                else:
                    if self.use_headers:
                        l = "\t".join(map(lambda x: str(x[0]), conn.description))
                        lines.append(l)

                    for a in result:
                        l = "\t".join(map(lambda x: str(x), a))
                        lines.append(l)

            return lines

