from kore.components.plugins.base import BasePluginComponent

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class BeakerCachePlugin(BasePluginComponent):

    def get_services(self):
        return (
            ('manager', self.manager),
        )

    def manager(self, container):
        config = container('kore.components.beaker.config')

        return CacheManager(**parse_cache_config_options(config))
