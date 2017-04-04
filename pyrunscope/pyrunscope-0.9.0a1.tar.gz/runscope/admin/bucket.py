from restkit import Resource

from runscope.model.resource import RunScopeResourceCollection

try:
    import simplejson as json
except ImportError:
    import json  # py2.6 only


# class Bucket(object):
#     def __init__(self, config):
#         self.config = config
#
#     def __getattr__(self, item):
#         if item in self.config:
#             return self.config[item]
#         else:
#             raise ValueError("Could not find attribute '" + item + "'.")
#
#     @property
#     def tests(self):
#         return TestCollectionResource(bucket_key=self.key).request()
#

# class Buckets(object):
#     def __init__(self, config):
#         self.data = config[u'data']
#
#     def filter(self, **filter_args):
#         for bucket_data in self.data:
#             yield Bucket(bucket_data)


class Bucket(Resource):
    resource_path = '/buckets/{bucket_key}'
    resource_method = 'get'

    def __init__(self, **kwargs):
        search_url = "https://api.runscope.com"
        super(Bucket, self).__init__(search_url, follow_redirect=True,
                                     max_follow_redirect=10, **kwargs)

    def search(self, query):
        return self.get('search.json', q=query)

    def request(self, *args, **kwargs):
        resp = super(Bucket, self).request(*args, **kwargs)
        return json.loads(resp.body_string())


class BucketCollection(RunScopeResourceCollection):
    resource_class = Bucket
    resource_path = '/buckets'
    resource_method = 'get'

