class Enum(object):
    '''
    An enum where the options are defined as ('slug', 'translation').

    It will be converted to just slug, with the translation in a 'choices' tuple.

    class Example(Enum):
        OPTION_A = ('a', _(u'Option A'))
        OPTION_B = ('b', _(u'Option B'))

    class ClassicExample(object):
        OPTION_A = 'a'
        OPTION_B = 'b'

        choices = (
            (OPTION_A, _(u'Option A')),
            (OPTION_B, _(u'Option B')),
        )
    '''
    class __metaclass__(type):
        def __new__(cls, name, bases, dict):
            new_dict = { '__module__': dict['__module__']  }
            choices = []
            for name, value in dict.items():
                if not name.startswith('_'):
                    new_dict[name] = value[0]
                    choices.append((value[0], value[1]))
            new_dict['choices'] = tuple(choices)

            return type.__new__(cls, name, bases, new_dict)
