import json
import time
import os
from tqdm import tqdm
from urllib import quote
from sqlshare_client.base import BaseObject

CHUNK_SIZE = 1000000
UPLOAD_PERCENT = 30


class Datasets(object):
    def __init__(self, oauth):
        self.oauth = oauth

    def mine(self):
        data = self.oauth.request("/v3/db/dataset/")
        return self._build_dataset_list(data)

    def shared(self):
        data = self.oauth.request("/v3/db/dataset/shared")
        return self._build_dataset_list(data)

    def all(self):
        data = self.oauth.request("/v3/db/dataset/all")
        return self._build_dataset_list(data)

    def get(self, owner, name):
        data = self.oauth.request("/v3/db/dataset/%s/%s" % (quote(owner),
                                                            quote(name)))
        return Dataset(json.loads(data))

    def get_permissions(self, owner, name):
        uri = "/v3/db/dataset/%s/%s/permissions"
        data = self.oauth.request(uri % (quote(owner), quote(name)))

        return Permissions(json.loads(data))

    def set_is_public(self, owner, name):
        uri = "/v3/db/dataset/%s/%s"
        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PATCH",
                                  body='{"is_public": true }')
        return data

    def set_is_private(self, owner, name):
        uri = "/v3/db/dataset/%s/%s"
        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PATCH",
                                  body='{"is_public": false }')
        return data

    def remove_sharing(self, owner, name):
        return self._set_sharing(owner, name, is_shared=False, is_public=False,
                                 accounts=[])

    def set_sharing(self, owner, name, accounts):
        return self._set_sharing(owner, name, is_shared=True, is_public=False,
                                 accounts=accounts)

    def _set_sharing(self, owner, name, is_public, is_shared, accounts):
        uri = "/v3/db/dataset/%s/%s/permissions"

        permissions = json.dumps({"is_public": is_public,
                                  "is_shared": is_shared,
                                  "authlist": accounts})

        data = self.oauth.request(uri % (quote(owner), quote(name)),
                                  method="PUT",
                                  body=permissions)
        return data

    def create_from_sql(self, owner, name, sql, description, is_public):
        # Force a true type value to be a boolean
        if is_public:
            is_public = True
        else:
            is_public = False
        ds_data = {
            "sql_code": sql,
            "is_public": is_public,
            "description": description,
        }
        data = self.oauth.request("/v3/db/dataset/%s/%s" % (quote(owner),
                                                            quote(name)),
                                  method="PUT",
                                  body=json.dumps(ds_data))

        return Dataset(json.loads(data))

    def create_from_file(self, owner, name, file_path, description, is_public,
                         visualize=False):
        if is_public:
            is_public = True
        else:
            is_public = False

        file_size = os.path.getsize(file_path)
        total_sent = 0
        handle = open(file_path)
        sample = handle.read(CHUNK_SIZE)
        last_percentage = 0

        upload_id = self.oauth.request("/v3/db/file/", method="POST",
                                       body=sample)

        total_sent += len(sample)

        # XXX - There should be options for changing the parser
        response = self.oauth.request("/v3/db/file/%s/parser" % upload_id)

        if visualize:
            pbar = tqdm(total=100)

        sample = handle.read(CHUNK_SIZE)
        while sample:
            self.oauth.request("/v3/db/file/%s" % upload_id, method="POST",
                               body=sample)

            total_sent += len(sample)

            percent_sent = float(total_sent) / float(file_size)
            current_percent = UPLOAD_PERCENT * percent_sent
            if visualize:
                diff = current_percent - last_percentage
                if diff > 0:
                    pbar.update(diff)
            last_percentage = current_percent

            sample = handle.read(CHUNK_SIZE)

        # Finalize the upload and poll...
        data = json.dumps({"dataset_name": name,
                           "description": description,
                           "is_public": is_public})

        finalize_url = "/v3/db/file/%s/finalize" % upload_id

        response = self.oauth.request(finalize_url,
                                      method="POST", body=data)

        data = json.loads(response)
        rows_total = data["rows_total"]
        rows_loaded = data["rows_loaded"]

        current_percent = float(rows_loaded) / float(rows_total)
        current_percent = (UPLOAD_PERCENT +
                           (100 - UPLOAD_PERCENT)*current_percent)

        if visualize:
            pbar.update(current_percent - last_percentage)
        last_percentage = current_percent

        while current_percent != 100:
            response = self.oauth.request(finalize_url)
            try:
                data = json.loads(response)
                rows_total = data["rows_total"]
                rows_loaded = data["rows_loaded"]
                current_percent = float(rows_loaded) / float(rows_total)

                current_percent = (UPLOAD_PERCENT +
                                   (100 - UPLOAD_PERCENT)*current_percent)

                if current_percent - last_percentage > 0:
                    if visualize:
                        pbar.update(current_percent - last_percentage)
                last_percentage = current_percent

            except Exception as ex:
                print "Error uploading file: %s" % response
            time.sleep(.5)
        if visualize:
            pbar.close()

    def _build_dataset_list(self, data):
        data = json.loads(data)
        datasets = []
        for value in data:
            datasets.append(Dataset(value))

        return datasets


class Permissions(object):
    def __init__(self, data={}):
        for key in data:
            if key == "accounts":
                setattr(self, key, map(lambda x: x["login"], data[key]))
            else:
                setattr(self, key, data[key])


class Dataset(BaseObject):
    def __str__(self):
        return "Dataset %s/%s" % (self.owner, self.name)

    def __cmp__(self, other):
        if self.owner < other.owner:
            return -1
        elif self.owner > other.owner:
            return 1

        if self.name < other.name:
            return -1
        if self.name > other.name:
            return 1

        return 0
