GENERATE = 'generate'
DELETE = 'delete'

__mode_map = {
    'generate': GENERATE,
    'gen': GENERATE,
    'g': GENERATE,
    'delete': DELETE,
    'del': DELETE,
    'd': DELETE,
}


def fetch_mode(mode_string):
    return __mode_map[mode_string] if mode_string in __mode_map else None
