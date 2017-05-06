# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="",
        # directory in the `nbextension/` namespace
        dest="corkboard",
        # _also_ in the `nbextension/` namespace
        require="corkboard/corkboard")]