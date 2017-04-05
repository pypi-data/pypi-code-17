from collections import OrderedDict
from functools import reduce, partial


def make_form(rng, root_name='ArchiveTransfer'):
    """Takes an rng,  returns a html form.

    Should be reworked.
    """
    results = rng.to_form()
    inside = results[root_name]

    def make_input(value):
        """ depending on what is found in the rng, make the input"""
        what = value[0]
        if what.startswith('not editable'):
            what = what.replace('not editable:', '').replace("'", "\'")
        if what.startswith('attribute:value:'):
            what = what.replace('attribute:value:', '').replace("'", "\'")
        return what

    def walk_dict(target_dict, depth=1):
        """ walks through the dict, makes a form"""
        stuff = ""

        def metadata_in_name(target_string, values):
            """serioulsy"""
            return 0 in [target_string.find(value) for value in values]

        for rng_key, rng_val in sorted(target_dict.items(), key=lambda x: x[0]):
            if isinstance(rng_val, dict):
                cssclass = ""
                if metadata_in_name(rng_key, ['zeroOrMore', 'oneOrMore']):
                    cssclass = "class='multiple'"
                clean_name = rng_key.replace('optional.', '').replace(
                            'oneOrMore.', '').replace('.data', '').replace(
                                'zeroOrMore.', '')
                stuff +="<div class=\"{0}\" >".format(clean_name)
                stuff += "<h{0} {2} rel='togglable' class=\"{3}_rel\">{1}<span class=\"nice-span glyphicon glyphicon-minus\"></span></h{0}>".format(depth, rng_key, cssclass, clean_name)
                stuff += "<div class='holder{}'>".format(depth)
                stuff += walk_dict(rng_val, depth + 1)
            else:
                def find_key(a_dict, key):
                    """find keys"""
                    for his_key, his_val in a_dict.items():
                        if isinstance(his_val, dict):
                            found = find_key(his_val, key)
                            if found:
                                return [his_key] + found
                        elif his_val == key:
                            return [his_key]

                def make_input_name(value):
                    """makes input name"""
                    values = ['optional', 'value',
                              'oneOrMore', 'data', "zeroOrMore"]

                    def strip_meta(this_string):
                        """removes metadata"""
                        wot = this_string.replace('optional', '').replace(
                            'oneOrMore', '').replace('.data', '').replace(
                                'zeroOrMore', '').replace('.', '')
                        return wot
                    ret = [strip_meta(tag) for tag in find_key(inside, value) if tag not in values]
                    return ".".join(ret)

                stuff += "\n<div class=\"{0}\"><div style='font-weight:bold;'>{1}</div>".format(
                                                                                     make_input_name(rng_val),
                    ".".join(find_key(inside, rng_val)))

                def val_starts_with(base_string, strings):
                    """ check if str startswith """
                    for the_string in strings:
                        if base_string.startswith(the_string):
                            return True
                if len(make_input(rng_val)) < 45:
                    if val_starts_with(rng_val[0], ['attribute:value:', 'not editable']):
                        stuff += "<input class='selectable' value=\"{}\" style='width:87%' name=\"{}\" readonly>".format(
                            make_input(rng_val), make_input_name(rng_val))
                    else:
                        stuff += "<input class='selectable' value=\"{}\" style='width:87%' name=\"{}\">".format(
                            "", make_input_name(rng_val))
                else:
                    if val_starts_with(rng_val[0], ['attribute:value:', 'not editable']):
                        stuff += "<textarea class='selectable' rows='8' cols='120' readonly name=\"{1}\">{0}</textarea>".format(
                            make_input(rng_val), make_input_name(rng_val))
                    else:
                        stuff += "<textarea class='selectable' rows='8' cols='120'>{0}</textarea>".format(
                            "")
                stuff += "</div>"
        stuff+="</div>"
        stuff += "</div>"
        return stuff
    return walk_dict(results)


def make_tree(dot_separated_keys):
    """Generates a dict of dicts from dot separated keys.

    Yet without associated values.
    For instance :
    {'a.b': 1, 'a.c': 2, 'b.d' : 1, 'b.e.a': 1, 'b.e.b': 2}
    would give you :
   {'a': {'c': {}, 'b': {}}, 'b': {'d': {}, 'e': {'b': {}, 'a': {}}}}
    """
    tree = {}
    for item in dot_separated_keys:
        inside_tree = tree
        for part in item.split('.'):
            inside_tree = inside_tree.setdefault(part, {})
    return tree


def set_in_nested_dict(empty, full):
    def get_from_dict(data_dict, map_list):
        """get from nested dict"""
        return reduce(lambda d, k: d[k], map_list, data_dict)

    def set_in_dict(data_dict, map_list, value):
        """set in nested dict"""
        target = get_from_dict(data_dict, map_list[:-1])
        if isinstance(target, dict):
            if len(target[map_list[-1]]) == 0 and isinstance(value, str):
                target[map_list[-1]] = value
            else:
                target[map_list[-1]]['value'] = value

    for key, val in full.items():
        set_in_dict(empty, key.split('.'), val)

    return True


def order_dicts(stuff, ordered=None, context=None):
    new_d = OrderedDict()
    for k, v in stuff.items():
        if isinstance(v, dict):
            new_d[k] = OrderedDict()
            top_level_order = []
            right = ""
            if not context:
                top_level_order = [value for key, value in ordered.items() if k in key][0]
            else:
                right = [item for item in context if k in item][0]
                top_level_order = [value for key, value in ordered.items() if right in key][0]
            weights = {e: i for i, e in enumerate(top_level_order) if e}

            def cond(sep, x, k):
                return x+sep in k

            final_cond = None
            if k not in stuff.keys():
                final_cond = partial(cond, "")
            else:
                final_cond = partial(cond, "_")
            top_level_key_list = sorted(stuff[k],key=lambda x : [v for k,v in weights.items() if final_cond(x,k)][0] if\
                                         len([ v for k,v in weights.items() if\
                                               final_cond(x,k)]) else\
                                         weights[x])
            for key in top_level_key_list:
                if right and right in stuff.keys():
                    k = right

                def is_a_dict(an_inside_d, an_order, k):
                    if isinstance(an_inside_d, dict):

                        order = ordered[k]
                        inside_d = OrderedDict()
                        for item in order:
                            if item in an_inside_d.keys():
                                inside_d[item]= is_a_dict(an_inside_d[item],order,item)
                            else:
                                print(item)
                        return inside_d
                    else:
                        return an_inside_d
                new_d[k][key] = is_a_dict(stuff[k][key],
                                          ordered[k],
                                          key)
            for clef in list(v.keys()):
                if isinstance(v[clef], dict):
                    with_suffix = [k for k in weights.keys() if clef+'_' in k]
                    clef2 = clef
                    if "_" not in clef and len(with_suffix) and with_suffix[0] in list(ordered.keys()) :
                        clef2 = with_suffix[0]
                    order_dicts(v[clef],
                                ordered=ordered,
                                context=ordered[clef2])
    return new_d


def dict_path(my_dict, path=None):
    """Flattens nested dicts into a single level dict.

    For instance :
    {'a': {'b': 1, 'c': 2}, 'b': {'d': 1, 'e': {'a': 1, 'b': 2}}}
    would give you :
    {'a.b': 1, 'a.c': 2, 'b.d' : 1, 'b.e.a': 1, 'b.e.b': 2}
    """
    if path is None:
        path = ""
    for k, v in my_dict.items():
        newpath = path + ("." if path != "" else "") + k
        if isinstance(v, dict):
            for u in dict_path(v, newpath):
                yield u
        else:
            yield newpath, v
