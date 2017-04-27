import io
import yaml
from sqlalchemy import create_engine


class Config(object):
    def __init__(self, config_path):
        self.config_path = config_path
        with io.open(config_path, 'r') as cfg:
            self.data = yaml.safe_load(cfg)
        application = self.data.get('application')
        database = self.data.get('db')
        self.BASE_URL = 'http://{host}{port}/v0'.format(**application)
        if database:
            self.DATABASE = 'postgresql://{user}:{pass}@{host}:{port}/{name}'.\
                format(**database)
            self.engine = create_engine(self.DATABASE, echo=True)
        self.APP_PORT = application.get('port')

    @property
    def application(self):
        return self.data.get('application')

    @property
    def db(self):
        return self.data.get('db')

    @property
    def redis_params(self):
        return self.data.get('redis_params')

    @property
    def session_params(self):
        return self.data.get('session_params')
