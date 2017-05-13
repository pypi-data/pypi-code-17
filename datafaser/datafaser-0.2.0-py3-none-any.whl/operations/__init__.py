from datafaser.operations import table, change, load, each, fill


def get_default_operations_map(data_tree):
    return {
        'load': load.Loader(data_tree).load,
        'table': table.convert,
        'change': change.map_keys,
        'each': each.convert,
        'fill': fill.convert
    }
