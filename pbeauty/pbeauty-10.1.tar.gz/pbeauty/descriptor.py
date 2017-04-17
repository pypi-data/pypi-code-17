# -*- coding: utf-8 -*-


class Descriptor(object):
    def __init__(self, name, comments):
        self.name = name
        self.comments = comments
        return

class FieldDescriptor(Descriptor):
    def __init__(self, lable, type, name, index, default, comments):
        Descriptor.__init__(self, name, comments)
        self.lable = lable
        self.type = type
        self.index = index
        self.default = default
        return

    def __str__(self):
        if self.default is not None:
            return '%s %s %s = %s [default = %s];' % (self.lable, self.type, self.name, self.index, self.default)
        else:
            return '%s %s %s = %s;' % (self.lable, self.type, self.name, self.index)

class MessageDescriptor(Descriptor):
    IS_ENUM = False
    def __init__(self, name, fields, comments):
        Descriptor.__init__(self, name, comments)
        self.fields = fields
        return

class EnumDescriptor(Descriptor):
    IS_ENUM = True
    def __init__(self, name, fields, comments):
        Descriptor.__init__(self, name, comments)
        self.fields = fields
        return

class PackageDescriptor(object):
    def __init__(self, filename, namespaces, imports, message_list):
        self.filename = filename
        self.namespaces = namespaces
        self.imports = imports
        self.message_list = message_list
        return

