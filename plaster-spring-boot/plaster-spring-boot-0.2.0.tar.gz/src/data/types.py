MODEL = 'model'
REPOSITORY = 'repository'
SERVICE = 'service'
CONTROLLER = 'controller'
FIELDS = 'fields'

ALL = [
    MODEL,
    REPOSITORY,
    SERVICE,
    CONTROLLER,
    FIELDS,
]

FILES = [
    MODEL,
    REPOSITORY,
    SERVICE,
    CONTROLLER,
]

FILES_WITH_FIELDS = [
    MODEL,
]

__type_map = {
    'scaffold': FILES,
}
for gen_type in ALL:
    __type_map[gen_type] = gen_type
__type_map[FIELDS] = FILES_WITH_FIELDS


def fetch_related_types(cat_string):
    related_types = __type_map[cat_string] if cat_string in __type_map else None
    if related_types and type(related_types) != list:
        related_types = [related_types]

    return related_types
