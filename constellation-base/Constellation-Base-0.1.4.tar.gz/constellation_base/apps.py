from django.apps import AppConfig


class ConstellationBaseConfig(AppConfig):
    name = 'constellation_base'

    def ready(self):
        from . import signals
