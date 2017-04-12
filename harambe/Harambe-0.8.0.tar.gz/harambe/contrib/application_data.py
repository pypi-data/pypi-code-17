"""
Application Data

K/V to store application data
"""


from harambe import (db, utils)
from six import string_types

def make_key(key):
    return utils.slugify(key)


class ApplicationData(db.Model):
    """
    Application Data
    """
    key = db.Column(db.String(250), index=True, unique=True)
    value = db.Column(db.JSONType)
    description = db.Column(db.String(250))

    @classmethod
    def get(cls, id, include_deleted=False, return_object=False):
        if isinstance(id, string_types) and id.isdigit():
            return super(cls, cls).get(id, include_deleted=include_deleted)

        key = make_key(id)
        r = cls.query().filter(key == key).first()
        if return_object:
            return r
        return r.value if r else {}

    @classmethod
    def upsert(cls, key, value, description=None, update_value=True):
        if not isinstance(value, dict):
            raise ValueError("Application Data value must be a dict")

        data = {"value": value}
        if description:
            data["description"] = description

        appset = cls.get(key, return_object=True)
        if appset:
            if update_value:
                v = appset.value
                v.update(value)
                data["value"] = v
            appset.update(**data)
        else:
            cls.create(key=make_key(key), **data)

