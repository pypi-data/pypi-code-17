

help_topic = 'Change operation'
help_text = '''
Change field names:

    - "Switch some keys while keeping old ones":
      - change:
          from:
            branch: "source with original keys"
          to:
            branch: "target with some keys changed"
          keys:
            old key: new key
            another old key: another new key
          others: keep

    - "Switch all keys and stop on missing ones":
      - change:
          from:
            branch: "source with original keys"
          to:
            branch: "target with all keys changed"
          keys:
            old key: new key
            another old key: another new key
          others: deny
'''


def map_keys(data_tree, directives):
    from_branch = directives['from']['branch']
    to_branch = directives['to']['branch']
    keymap = directives['keys']
    others = directives.get('others', 'deny')
    source = data_tree.reach(from_branch)

    if others == 'keep':
        target = map_keys_keep(keymap, source)
    else:
        target = map_keys_deny(keymap, source)

    data_tree.merge(target, to_branch)


def map_keys_keep(keymap, source):
    target = {}
    for key, value in source.items():
            target[keymap.get(key, key)] = value
    return target


def map_keys_deny(keymap, source):
    target = {}
    denied = []

    for key, value in source.items():
        if key in keymap:
            target[keymap[key]] = value
        else:
            denied.append(key)

    if len(denied):
        raise KeyError('Unmatched keys: "' + '", "'.join(denied) + '"')

    return target
