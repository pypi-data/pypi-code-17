
import inspect
from harambe import (register_package,
                     get_config,
                     decorators as h_deco,
                     abort)


# `contrib` prefix is set so all templates in this package
# get accessed via `contrib/`
register_package(__package__, "contrib")


# ------------------------------------------------------------------------------

# AREA51

AREA51_LAYOUT = "contrib/area51/layout.jade"

AREA51_TAG = "AREA51"

def disable_area51(*a, **kw):
    abort(404)

# @area51
def area51(f):
    """
    @area51
    A decorator that turns a class into ADMIN
    """
    import auth.decorators as a_deco

    if not inspect.isclass(f):
        raise TypeError("@AREA51 expects a Harambe class")

    if get_config("AREA51_ENABLED", True):

        # ROLES
        min_role = get_config("AREA51_MIN_ACL", "ADMIN")
        role_name = "accepts_%s_roles" % min_role.lower()

        if not hasattr(a_deco, role_name):
            raise ValueError("Invalid AREA51_MIN_ACL: %s" % min_role)

        getattr(a_deco, role_name)(f)
        a_deco.login_required(f)

        f._nav_tags = [AREA51_TAG]
        layout = get_config("AREA51_LAYOUT") or AREA51_LAYOUT
        return h_deco.template(layout=layout)(f)

    else:
        f._nav_visible = False
        f.before_request = disable_area51
        return f

