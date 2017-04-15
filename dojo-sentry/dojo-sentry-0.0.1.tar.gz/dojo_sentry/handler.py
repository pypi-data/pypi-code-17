from __future__ import unicode_literals

from raven import Client


class SentryHandler(object):

    def __init__(self, config, secrets, dataset):
        self.config = config
        self.secrets = secrets
        self.dataset = dataset

    def capture(self, e):
        client = Client(self.secrets['sentry_dsn'])
        client.captureException(extra={'dataset': self.dataset})
