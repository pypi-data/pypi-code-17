import json

from django.contrib.postgres.forms.jsonb import InvalidJSONInput, JSONField


class JSONPrettyField(JSONField):
    def __init__(self, *args, **kwargs):
        self.__indent = kwargs.pop('indent', 2)
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value, indent=self.__indent, sort_keys=True, ensure_ascii=False)
