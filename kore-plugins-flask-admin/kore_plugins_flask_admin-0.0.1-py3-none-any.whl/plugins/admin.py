import logging

from flask_admin import Admin

from kore.components.plugins.base import BasePluginComponent

log = logging.getLogger(__name__)


class FlaskAdminPluginComponent(BasePluginComponent):

    def get_services(self):
        return (
            ('config', self.config),
            ('admin', self.admin),
        )

    def config(self, container):
        config = container('config')

        return config.get('flask_admin', {})

    def admin(self, container):
        config = container('kore.components.flask_admin.config')

        template_mode = config.get('template_name', None)

        return Admin(template_mode=template_mode)

    def post_hook(self, container):
        app = container('kore.components.flask.application')
        admin = container('kore.components.flask_admin.admin')

        admin.init_app(app)
