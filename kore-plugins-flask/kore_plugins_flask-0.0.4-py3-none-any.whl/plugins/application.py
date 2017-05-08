import logging

from flask import Flask

from kore.components.plugins.base import BasePluginComponent

log = logging.getLogger(__name__)


class FlaskApplicationPluginComponent(BasePluginComponent):

    def get_services(self):
        return (
            ('config', self.config),
            ('application', self.application),
        )

    def config(self, container):
        config = container('config')

        return config.get('flask', {})

    def application(self, container):
        config = container('kore.components.flask.config')

        instance_path = config.get('instance_path', None)
        root_path = config.get('root_path', None)

        app = Flask(
            __name__,
            instance_path=instance_path,
            root_path=root_path,
        )
        app.config.from_mapping(**config)
        return app
