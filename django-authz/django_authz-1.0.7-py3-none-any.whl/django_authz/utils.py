from fnmatch import fnmatch
from django.apps import apps

_registry = {}


def get_role_implementation(role_short_name):
    try:
        return _registry[role_short_name]
    except:
        print(("Error: role name %s not in registry" % role_short_name))
        return None


def force_to_model(model):
    """ Return model class """
    if isinstance(model, str):
        rv = apps.get_model(model)
    else:
        rv = model
    #print("%s converted to model: %s" % (model,rv))
    return rv


def get_model_full_name(model):
    if isinstance(model, str):
        return model
    return "%s.%s" % (model._meta.app_label.lower(), model._meta.model_name.lower())


def wlist_blist(src_list, white_list, black_list):
    """ Return items from src_list which match any of pattern from white_list
        and remove all matching any of black_list"""
    if white_list:
        rv = []
        for item in src_list:
            for pattern in white_list:
                if fnmatch(item, pattern):
                    rv.append(item)
                    break
    else:
        rv = src_list
    if not black_list:
        return rv
    for item in rv[:]:
        for pattern in black_list:
            if fnmatch(item, pattern):
                rv.remove(item)
                break
    print(("wlist_blist(%s,%s,%s) = %s" % (src_list, white_list, black_list, rv)))
    return rv
