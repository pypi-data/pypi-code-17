from kore.components.plugins.base import BasePluginComponent


class BeakerPlugin(BasePluginComponent):

    def get_services(self):
        return (
            ('config', self.config),
        )

    def config(self, container):
        config = container('config')

        return config.get('beaker', {})
