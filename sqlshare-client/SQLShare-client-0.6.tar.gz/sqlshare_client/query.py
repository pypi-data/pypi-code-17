import json
import time
from sqlshare_client.base import BaseObject


class Query(object):
    def __init__(self, oauth):
        self.oauth = oauth

    def get_all(self):
        data = self.oauth.request("/v3/db/query")
        queries = json.loads(data)
        results = []
        for q in queries:
            results.append(QueryInstance(q))
        return results

    def run_query(self, sql):
        q = self.launch_query(sql)

        delay = 0.01
        while not q.is_finished:
            self.poll_query(q)
            time.sleep(delay)

            if delay < 2.0:
                delay *= 2

        return q

    def launch_query(self, sql):
        req = json.dumps({"sql": sql})
        data = self.oauth.request("/v3/db/query",
                                  method="POST",
                                  body=req
                                  )
        return QueryInstance(json.loads(data))

    def poll_query(self, query_instance):
        url = query_instance.url
        data = self.oauth.request(url)
        query_instance.set_attributes_from_data(json.loads(data))


class QueryInstance(BaseObject):
    pass
