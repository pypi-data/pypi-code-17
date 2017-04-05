"""
Application Data

K/V to store application data
"""


from harambe import (db, utils)


def make_key(key):
    return utils.slugify(key)


class ApplicationData(db.Model):
    """
    Application Data
    """
    key = db.Column(db.String(250), index=True, unique=True)
    data = db.Column(db.JSONType)
    description = db.Column(db.String(250))


    @classmethod
    def get_by_key(cls, key):
        key = make_key(key)
        return cls.query().filter(key == key).first()

    @classmethod
    def get_key(cls, key):
        d = cls.get_by_key(key)
        return {} if not d else d.data

    @classmethod
    def set_key(cls, key, value, description=None):
        if not isinstance(value, dict):
            raise ValueError("Application Data value must be a dict")

        data = {"data": value}
        if description:
            data["description"] = description

        appset = cls.get_by_key(key)
        if appset:
            appset.update(**data)
        else:
            cls.create(key=make_key(key), **data)
