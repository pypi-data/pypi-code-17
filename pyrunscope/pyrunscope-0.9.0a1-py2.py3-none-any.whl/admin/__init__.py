from runscope.admin.bucket import BucketCollection


class Admin(object):
    def __getattr__(self, item):
        if item == 'buckets':
            return BucketCollection()
