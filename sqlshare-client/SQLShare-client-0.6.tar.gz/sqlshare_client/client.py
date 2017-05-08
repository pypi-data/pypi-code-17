from sqlshare_client.oauth import OAuth
from sqlshare_client.datasets import Datasets
from sqlshare_client.users import Users
from sqlshare_client.query import Query


class Client(object):
    def __init__(self, oauth_id, oauth_secret, server=None, redirect_uri=None,
                 grant_type=None):
        self.oauth = OAuth(oauth_id, oauth_secret, server, redirect_uri,
                           grant_type)

    def has_access(self):
        return self.oauth.has_access()

    def get_authorize_url(self):
        return self.oauth.get_authorize_url()

    def get_tokens_for_code(self, code):
        return self.oauth.request_token(code)

    def get_my_datasets(self):
        return Datasets(self.oauth).mine()

    def get_shared_datasets(self):
        return Datasets(self.oauth).shared()

    def get_all_datasets(self):
        return Datasets(self.oauth).all()

    def get_dataset(self, owner, name):
        return Datasets(self.oauth).get(owner, name)

    def get_permissions(self, owner, name):
        return Datasets(self.oauth).get_permissions(owner, name)

    def set_is_public(self, owner, name):
        return Datasets(self.oauth).set_is_public(owner, name)

    def set_is_private(self, owner, name):
        return Datasets(self.oauth).set_is_private(owner, name)

    def remove_sharing(self, owner, name):
        return Datasets(self.oauth).remove_sharing(owner, name)

    def set_shared(self, owner, name, accounts):
        return Datasets(self.oauth).set_sharing(owner, name, accounts)

    def run_query(self, sql):
        return Query(self.oauth).run_query(sql)

    def get_all_queries(self):
        return Query(self.oauth).get_all()

    def get_current_user(self):
        return Users(self.oauth).get_current_user()

    def create_dataset_from_sql(self, owner, name, sql,
                                description, is_public):
        return Datasets(self.oauth).create_from_sql(owner, name, sql,
                                                    description,
                                                    is_public)

    def create_dataset_from_file(self, owner, name, file_path,
                                 description, is_public, visualize=False):
        return Datasets(self.oauth).create_from_file(owner, name, file_path,
                                                     description,
                                                     is_public,
                                                     visualize)
