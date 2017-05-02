import click


class KeyValue(click.ParamType):
    name = 'key=value'

    def convert(self, value, param, ctx):
        value_split = value.split('=')
        if len(value_split) != 2:
            self.fail("{} is not a valid key=value".format(value), param, ctx)
        key, value = value_split
        return key, value


KEY_VALUE = KeyValue()
