from slugify import slugify


class Story(object):
    def __init__(self, name, properties=None):
        self._name = name
        self._properties = properties

    @property
    def name(self):
        return self._name

    @property
    def slug(self):
        return slugify(self._name)

    @property
    def properties(self):
        return self._properties

    @property
    def filename(self):
        return self._filename


class HitchStory(Story):
    def __init__(self, engine):
        from hitchstory import BaseEngine
        assert isinstance(engine, BaseEngine)
        self._name = engine.story.name
        self._filename = engine.story.filename
        self._properties = engine.story.about
        self._properties['preconditions'] = engine.story.preconditions
