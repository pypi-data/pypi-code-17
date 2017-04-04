import json
import os, runscope
from unittest import TestCase


class TestRSBucket(TestCase):

    # def test_bucket(self):
    #     runscope.set_defaults(
    #         client_id=os.environ['RS_CLIENT_ID'],
    #         access_token=os.environ['RS_ACCESS_TOKEN']
    #     )
    #
    #     client = runscope.client('admin')
    #     for bucket in client.buckets.filter():
    #         print "Found Bucket: {name}".format(name=bucket.name)
    #         for test in bucket.tests.all():
    #             print " - {name}".format(name=test.name)
    #             for step in test.steps.all():
    #                 print "  - {name}".format(name=step.id)
    #         print "\n"

    def test_results(self):
        runscope.set_defaults(
            client_id=os.environ['RS_CLIENT_ID'],
            access_token=os.environ['RS_ACCESS_TOKEN']
        )

        client = runscope.client('admin')
        for bucket in client.buckets.filter():
            print "Found Bucket: {name}".format(name=bucket.name)
            for test in bucket.tests.all():
                for result in test.results.all():
                    print result.finished_at
                    print json.dumps(dict(result), indent=4, default=str)
