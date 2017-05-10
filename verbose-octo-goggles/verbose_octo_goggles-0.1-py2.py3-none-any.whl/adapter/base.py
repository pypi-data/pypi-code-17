class Adapter(object):

    def upsert(self, data):
        raise NotImplementedError

    def delete(self, data):
        raise NotImplementedError

    def get(self, pk):
        raise NotImplementedError
