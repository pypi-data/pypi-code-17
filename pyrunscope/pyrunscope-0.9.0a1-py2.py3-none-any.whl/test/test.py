from restkit import Resource

import runscope

try:
    import simplejson as json
except ImportError:
    import json  # py2.6 only


class Test(object):
    def __init__(self, config):
        self.config = config

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]
        else:
            raise ValueError("Could not find attribute '" + item + "'.")

class Tests(object):
    def __init__(self, config):
        self.data = config[u'data']

    def filter(self, **filter_args):
        for bucket_data in self.data:
            yield Test(bucket_data)


class TestResource(Resource):
    def __init__(self, **kwargs):
        search_url = "https://api.runscope.com"
        super(TestResource, self).__init__(search_url, follow_redirect=True,
                                             max_follow_redirect=10, **kwargs)

    def search(self, query):
        return self.get('search.json', q=query)

    def request(self, *args, **kwargs):
        resp = super(TestResource, self).request(*args, **kwargs)
        return json.loads(resp.body_string())


class TestCollectionResource(Resource):
    def __init__(self, bucket_key, **kwargs):
        search_url = "https://api.runscope.com"
        super(TestCollectionResource, self).__init__(search_url, follow_redirect=True,
                                                       max_follow_redirect=10, **kwargs)
        self.bucket_key = bucket_key

    def search(self, query):
        return self.get('search.json', q=query)

    def request(self, *args, **kwargs):
        url = '/buckets/'+self.bucket_key+'/tests'
        resp = super(TestCollectionResource, self).request('GET', url, headers={
            'Authorization': "Bearer " + runscope.get_defaults()['access_token']
        })
        return Tests(json.loads(resp.body_string()))
