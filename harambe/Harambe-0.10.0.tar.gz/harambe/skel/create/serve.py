"""
________________________________________________________________________________


 /$$   /$$                                            /$$
| $$  | $$                                           | $$
| $$  | $$  /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$/$$$$ | $$$$$$$   /$$$$$$
| $$$$$$$$ |____  $$ /$$__  $$|____  $$| $$_  $$_  $$| $$__  $$ /$$__  $$
| $$__  $$  /$$$$$$$| $$  \__/ /$$$$$$$| $$ \ $$ \ $$| $$  \ $$| $$$$$$$$
| $$  | $$ /$$__  $$| $$      /$$__  $$| $$ | $$ | $$| $$  | $$| $$_____/
| $$  | $$|  $$$$$$$| $$     |  $$$$$$$| $$ | $$ | $$| $$$$$$$/|  $$$$$$$
|__/  |__/ \_______/|__/      \_______/|__/ |__/ |__/|_______/  \_______/



https://github.com/mardix/harambe

________________________________________________________________________________
"""

from harambe import HarambeApp

# == CLI ==
# Import your app cli. Omit if it will not be used
import app.cli


# == PROJECTS ==
# Projects is a dict with list of views that will be loaded by name
# ie: `app=main happy :serve` will serve all the views in the `main` list
# Views are placed in app/views directory, and should be listed as string
# without the `.py`
# You can add as many projects as you want, containing as many views
# It also allows you to use multiple config env
# ie: `app=main:production happy:serve` will use the `main` project with
# `production` config
projects = {
    "main": [
        "main"
    ]
}

# == INIT ==
# Init the application
# 'happy' variable is mandatory if you plan on using the happy cli
happy = HarambeApp(__name__, projects)

