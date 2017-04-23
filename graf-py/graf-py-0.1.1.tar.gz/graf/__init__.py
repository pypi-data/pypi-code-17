from .client import Client
instance = Client.instance()
measure = instance.measure
__all__ = ['Client', 'instance', 'measure']
