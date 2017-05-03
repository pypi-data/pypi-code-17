import couchdb
import re
import urllib.parse


class DocumentsAdmin(object):
    """ Supports management of TractDB documents.
    """

    def __init__(self, couchdb_url, couchdb_user, couchdb_user_password):
        """ Create an admin object.
        """
        self._couchdb_url = couchdb_url
        self._couchdb_user = couchdb_user
        self._couchdb_user_password = couchdb_user_password

    def create_document(self, doc, doc_id=None):
        """ Add a document to a database.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        # Get the database for the user
        database = server[dbname]

        # Set id for the document
        doc = dict(doc)
        if doc_id:
            doc['_id'] = doc_id

        # Store the document
        created_id, created_rev = database.save(doc)

        doc['_id'] = created_id
        doc['_rev'] = created_rev

        return doc

    def get_document(self, doc_id):
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        doc = database[doc_id]

        # Return as a dict, not our couchdb internal object
        return dict(doc)

    def update_document(self, doc):
        """ Update a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Update the document
        try:
            result = database.save(doc)
        except couchdb.http.ResourceConflict:
            raise Exception('Document "{:s} was modified.'.format(doc['_id']))

        return result

    def delete_document(self, doc_id):
        """ Delete a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        # Delete it
        del database[doc_id]

    def list_documents(self):
        """ List the id of all the documents of the given account.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Return all document ids
        return [doc for doc in database]

    def _format_server_url(self):
        """ Format the base URL we use for connecting to the server.
        """
        return '{}://{:s}:{:s}@{:s}'.format(
            urllib.parse.urlparse(self._couchdb_url).scheme,
            self._couchdb_user,
            self._couchdb_user_password,
            self._couchdb_url[
                len(urllib.parse.urlparse(self._couchdb_url).scheme) + len('://')
                :
            ]
        )

    @property
    def _couchdb_databases(self):
        """ List what CouchDB databases exist.
        """
        server = self._couchdb_server

        # Our databases are defined by the user name plus the suffix '_tractdb'
        pattern = re.compile('.*_tractdb')
        dbnames = [dbname for dbname in server if pattern.match(dbname)]

        return dbnames

    @property
    def _couchdb_users(self):
        """ List what CouchDB users exist.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']

        # This is our docid pattern
        pattern = re.compile('org\.couchdb\.user:(.*)')

        # Keep only the users that match our pattern, extracting the user
        users = []
        for docid in database_users:
            match = pattern.match(docid)
            if match:
                account_user = match.group(1)
                users.append(account_user)

        return users

    @property
    def _couchdb_server(self):
        return couchdb.Server(self._format_server_url())
