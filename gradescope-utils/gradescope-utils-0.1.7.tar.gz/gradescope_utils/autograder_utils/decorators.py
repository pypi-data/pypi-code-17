class weight(object):
    """Simple decorator to add a __weight__ property to a function

    Usage: @weight(3.0)
    """
    def __init__(self, val):
        self.val = val

    def __call__(self, func):
        func.__weight__ = self.val
        return func


class visibility(object):
    """Simple decorator to add a __visibility__ property to a function

    Usage: @visibility("hidden")

    Options for the visibility field are as follows:

    - `hidden`: test case will never be shown to students
    - `after_due_date`: test case will be shown after the assignment's due date has passed
    - `after_published`: test case will be shown only when the assignment is explicitly published from the "Review Grades" page
    - `visible` (default): test case will always be shown
    """

    def __init__(self, val):
        self.val = val

    def __call__(self, func):
        func.__visibility__ = self.val
        return func


class tags(object):
    """Simple decorator to add a __tags__ property to a function

    Usage: @tags("concept1", "concept2")
    """
    def __init__(self, *args):
        self.tags = args

    def __call__(self, func):
        func.__tags__ = self.tags
        return func
