from .base import Adapter


class EmptyAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        pass

    def get(self, pk):
        pass

    def upsert(self, data):
        pass

    def delete(self, data):
        pass

