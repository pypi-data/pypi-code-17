"""
Written by: Ian Doarn

Exceptions used by zbsmsa
"""


class SiteNotLoaded(Exception):
    def __init__(self, msg=None):
        if msg is None:
            message = "Can not login to website. webdriver has not been started."
        else:
            message = "{}. webdriver has not been started".format(msg)
        super(SiteNotLoaded, self).__init__(message)
        self.message = str(message)


class LoginFailed(Exception):
    def __init__(self, reason, msg=None, parent=None):
        if parent is None:
            raise ValueError("parent error can not be NoneType.")
        if msg is None:
            message = "Can not login to website: {}. [{}]".format(reason, parent)
        else:
            message = "{}. {}. [{}]".format(msg, reason, parent)
        super(LoginFailed, self).__init__(message)
        self.reason = reason
        self.parent_error = parent
        self.message = str(message)


class InvalidRange(Exception):
    def __init__(self, given_range, msg=None):
        if msg is None:
            message = "Given range is not valid for formatting Input: [{}]".format(given_range)
        else:
            message = "{}. Input: [{}]".format(msg, given_range)
        super(InvalidRange, self).__init__(message)
        self.message = str(message)
        self.given_range = given_range


class ItemAddError(Exception):
    def __init__(self, product, input_location='product chooser', msg=None):
        if msg is None:
            message = "Unable to add {} to {}. " \
                      "Please resolve this issue manually".format(product, input_location)
        else:
            message = "Unable to add {} to {}. {}. " \
                      "Please resolve this issue manually".format(product, input_location, msg)
        super(ItemAddError, self).__init__(message)
        self.message = str(message)
        self.product = product
        self.input_location = input_location


class ItemSelectError(Exception):
    def __init__(self, product, location, msg=None):
        if msg is None:
            message = "Unable to select {} on {}. Please resolve this issue manually".format(product, location)
        else:
            message = "Unable to select {} on {}. {}. " \
                      "Please resolve this issue manually".format(product, location, msg)
        super(ItemSelectError, self).__init__(message)
        self.message = str(message)
        self.product = product
        self.location = location


class ItemFindError(Exception):
    def __init__(self, product, location, msg=None):
        if msg is None:
            message = "Unable to find {} in {}. Please resolve this issue manually".format(product, location)
        else:
            message = "Unable to find {} in {}. {}. " \
                      "Please resolve this issue manually".format(product, location, msg)
        super(ItemFindError, self).__init__(message)
        self.message = str(message)
        self.product = product
        self.location = location


class SelectionError(Exception):
    def __init__(self, location, msg=None):
        if msg is None:
            message = "Unable to select {}. Please resolve this issue manually".format(location)
        else:
            message = "Unable to select {}. {}. " \
                      "Please resolve this issue manually".format(location, msg)
        super(SelectionError, self).__init__(message)
        self.message = str(message)
        self.location = location
