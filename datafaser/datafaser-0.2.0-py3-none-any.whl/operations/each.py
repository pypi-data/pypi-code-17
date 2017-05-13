from jinja2 import Template
import datafaser.operations


help_topic = 'Each operation'
help_text = '''
Do an operation for each list member:

    - "Change field names in all list members":
        - each:
          from:
            branch: "objects from spreadsheet"
          to:
            branch: "objects with new names"
          do:
            change:
              keys:
                old key: new key
              others: keep

Operation under "do" is used to produce an item to to.branch from each item in from.branch:

    objects from spreadsheet:
      - my key: value 1 on row 1
        old key: value 2 on row 1
      - my key: value 1 on row 2
        old key: value 2 on row 2
        
    objects with new names:
      - my key: value 1 on row 1
        new key: value 2 on row 1
      - my key: value 1 on row 2
        new key: value 2 on row 2
'''


def convert(data_tree, directives):
    from_branch = directives['from']['branch']
    to = directives.get('to', {})
    has_to_branch = 'branch' in to
    to_branch = to.get('branch', None)

    operation_name = list(directives['do'].keys())[0]
    operation_directives = directives['do'][operation_name]
    operation = datafaser.operations.get_default_operations_map(data_tree)[operation_name]

    source = data_tree.reach(from_branch)

    if isinstance(source, list):
        keys = range(0, len(source))
        collection_type = list
    else:
        keys = source.keys()
        collection_type = dict

    if has_to_branch:
        data_tree.merge(collection_type(), to_branch)
        target = data_tree.reach(to_branch)

    for key in keys:
        value = source[key]
        if has_to_branch:
            value_class = value.__class__
            if collection_type is list:
                target.append(value_class())
            else:
                target[key] = value_class()

        template_values = { 'key': key, 'value': value, 'data': data_tree.data }

        call_directives = _render_all_strings(operation_directives, template_values)
        call_directives['from'] = {'branch': [from_branch, key]}
        if has_to_branch:
            call_directives['to'] = {'branch': [to_branch, key]}

        operation(data_tree, call_directives)


def _render_all_strings(branch, data):
    if isinstance(branch, str):
        return Template(branch).render(data)
    elif isinstance(branch, dict):
        return {_render_all_strings(key, data): _render_all_strings(value, data) for key, value in branch.items()}
    elif isinstance(branch, list):
        return [_render_all_strings(value, data) for value in branch]
    return branch
