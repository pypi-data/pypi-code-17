from unqlite import UnQLite


class QueryObject(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def all(self):
        pass

    def create(self, body):
        pass

    def get(self, pk):
        pass

    def delete(self, pk):
        pass

    def update(self, pk, body):
        pass


class MemoryQueryObject(QueryObject):
    def __init__(self, collection_name):
        super(MemoryQueryObject, self).__init__(collection_name)

        self.objects = dict()
        self.current_pk = 0

    def all(self):
        return self.objects.values()

    def create(self, body):
        if 'pk' in body:
            # throw exception.
            pass

        body = self._assign_pk(body)
        self.objects[self.current_pk] = body
        self.current_pk += 1
        return body

    def get(self, pk):
        if pk in self.objects:
            return self.objects[pk]
        return None

    def delete(self, pk):
        obj = self.get(pk)
        del self.objects[pk]
        return obj

    def update(self, pk, body):
        self.objects[pk].update(body)
        return self.objects[pk]

    def _assign_pk(self, body):
        body = body.copy()
        body['pk'] = self.current_pk
        return body


class UnQLiteQueryObject(QueryObject):
    db = UnQLite('db.unqlite')

    def __init__(self, collection_name):
        super(UnQLiteQueryObject, self).__init__(collection_name)

        self.collection = self.db.collection(self.collection_name)

        # create if the collection does not exists.
        self.collection.create()

    def all(self):
        return self.collection.all()

    def create(self, body, pk=None):
        """
        :param: pk pass a pk to create or update if it exists.
        """
        if pk is not None:
            previous = self.collection[pk]
            if previous is not None:
                return self.update(pk, body)

        pk = self.collection.store(body)
        return self.get(pk)

    def get(self, pk):
        return self.collection[pk]

    def delete(self, pk):
        obj = self.get(pk)
        self.collection.delete(pk)
        return obj

    def update(self, pk, body):
        self.collection.update(pk, body)
        return self.get(pk)

    def filter(self, condition):
        return self.collection.filter(condition)
