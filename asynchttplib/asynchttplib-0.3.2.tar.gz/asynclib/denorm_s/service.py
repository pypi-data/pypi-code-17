from asynclib.denorm_s.db import DenormDBManager
from asynclib.service import Service, ServiceConfig


class DenormService(Service):

    def __init__(self, mongo_url):
        super(DenormService, self).__init__(ServiceConfig('denorm', mongo_url))

    def get_query_db(self, *args, **kwargs):
        return DenormDBManager(self.mongo)

    def run(self):
        self.run_private_api()