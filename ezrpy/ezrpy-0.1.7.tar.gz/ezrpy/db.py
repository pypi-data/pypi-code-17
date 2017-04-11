from tinydb import TinyDB

from ezrpy.error import RequestError


class Database(object):
    def query_object(self, collection_name):
        raise NotImplementedError()


class QueryObject(object):
    def all(self):
        """
        Gets all documents in this collection.

        :return: a list of documents.
        """
        raise NotImplementedError()

    def create(self, body, pk=None):
        """
        Creates a new document, only if the pk does not exists.

        :param pk: id to test if the document already exists, aborting if it
                   does.
        :param body: document to store.
        :return: the stored document.
        """
        raise NotImplementedError()

    def get(self, pk):
        """
        Gets an specific document by id.

        :param pk: id of the document to get.
        :return: the document.
        """
        raise NotImplementedError()

    def delete(self, pk):
        """
        Deletes an existing document.

        :param pk: id of the document to delete.
        :return: the deleted document.
        """
        raise NotImplementedError()

    def update(self, pk, body):
        """
        Updates an existing document.

        :param pk: document to update.
        :param body: new document body.
        :return: the new document.
        """
        raise NotImplementedError()


class TinyBDDatabase(Database):
    def __init__(self, path):
        self.db = TinyDB(path)

    def query_object(self, collection_name):
        table = self.db.table(collection_name)

        return TinyDBQueryObject(table)


class TinyDBQueryObject(QueryObject):
    def __init__(self, table):
        self.table = table

    def all(self):
        docs = []
        for raw_document in self.table.all():
            document = dict(raw_document)
            document['id'] = raw_document.eid
            docs.append(document)
        return docs

    def get(self, pk):
        raw_document = self.table.get(eid=pk)
        if raw_document is None:
            raise RequestError(404, 'document not found: %d' % pk)

        document = dict(raw_document)
        document['id'] = raw_document.eid
        return document

    def create(self, body, pk=None):
        if pk is not None and self.table.contains(eids=[pk]):
            return self.get(pk)

        pk = self.table.insert(body)

        # TODO: is this a performance concern?
        return self.get(pk)

    def update(self, pk, body):
        pk = self.table.update(body, eids=[pk])

        # TODO: is this a performance concern?
        return self.get(pk)

    def delete(self, pk):
        document = self.get(pk)

        self.table.remove(eids=[pk])
        return document
