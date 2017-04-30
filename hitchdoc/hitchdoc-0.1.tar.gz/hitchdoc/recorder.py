from hitchdoc.database import Database
from hitchdoc import exceptions
import pickle
import base64


class Recorder(object):
    def __init__(self, story, sqlite_filename):
        self._story = story
        self._db = Database(sqlite_filename)

        self._model = self._db.Recording(
            name=story.name,
            slug=story.slug,
            properties=base64.b64encode(pickle.dumps(story.properties))
        )
        self._model.save(force_insert=True)

    def step(self, name, **kwargs):
        for key, value in kwargs.items():
            assert type(key) is str

            try:
                pickle.dumps(value)
            except TypeError:
                raise exceptions.VarMustBePickleable(
                    "Can't use non-pickleable objects as vars."
                )

        new_step = self._db.Step(
            recording=self._model,
            name=name,
            kwargs=base64.b64encode(pickle.dumps(kwargs))
        )
        new_step.save()
