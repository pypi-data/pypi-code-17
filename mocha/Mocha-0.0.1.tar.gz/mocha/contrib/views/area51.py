"""
views.area51 is a basic home page for your admin area
"""

from harambe import (Harambe,
                     decorators as deco,
                     )

import harambe.contrib


@deco.route("/admin/")
@harambe.contrib.area51
class Admin(Harambe):

    @deco.template("contrib/area51/Admin/index.jade")
    @deco.nav_title("Admin Home", tags=harambe.contrib.AREA51_TAG, attach_to=["harambe.contrib.views.auth.Account", "self"])
    def index(self):
        return

